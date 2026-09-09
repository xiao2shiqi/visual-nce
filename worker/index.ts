/**
 * Cloudflare Workers Static Assets 不提供分段传输：请求带 Range 也返回
 * 200 + 完整文件，响应头没有 Accept-Ranges。浏览器据此把音频标记为
 * seekable = [0, 0]，于是 audio.currentTime 赋值全部无效——线上表现就是
 * 点台词跳句、拖进度条、方向键快退全都不动，只能从头听到尾。
 *
 * 这里只接管 /audio/，从资源层取完整文件后自行切片响应。
 */

interface Env {
  ASSETS: Fetcher;
}

interface ByteRange {
  start: number;
  end: number;
}

const parseRange = (header: string, size: number): ByteRange | null => {
  const match = /^bytes=(\d*)-(\d*)$/.exec(header.trim());
  if (!match) return null;

  const [, rawStart, rawEnd] = match;
  let start: number;
  let end: number;

  if (rawStart === '') {
    // bytes=-N：请求最后 N 个字节
    const suffix = Number(rawEnd);
    if (!Number.isInteger(suffix) || suffix <= 0) return null;
    start = Math.max(0, size - suffix);
    end = size - 1;
  } else {
    start = Number(rawStart);
    end = rawEnd === '' ? size - 1 : Number(rawEnd);
  }

  if (!Number.isInteger(start) || !Number.isInteger(end)) return null;
  if (start < 0 || start >= size || end < start) return null;

  return { start, end: Math.min(end, size - 1) };
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (!url.pathname.startsWith('/audio/')) {
      return env.ASSETS.fetch(request);
    }

    const assetResponse = await env.ASSETS.fetch(new Request(url.toString(), { method: 'GET' }));
    if (!assetResponse.ok) return assetResponse;

    const body = await assetResponse.arrayBuffer();
    const size = body.byteLength;
    const headers = new Headers(assetResponse.headers);
    headers.set('Accept-Ranges', 'bytes');

    const isHead = request.method === 'HEAD';
    const rangeHeader = request.headers.get('Range');

    if (!rangeHeader) {
      headers.set('Content-Length', String(size));
      return new Response(isHead ? null : body, { status: 200, headers });
    }

    const range = parseRange(rangeHeader, size);
    if (!range) {
      headers.set('Content-Range', `bytes */${size}`);
      return new Response(null, { status: 416, headers });
    }

    headers.set('Content-Range', `bytes ${range.start}-${range.end}/${size}`);
    headers.set('Content-Length', String(range.end - range.start + 1));
    return new Response(isHead ? null : body.slice(range.start, range.end + 1), {
      status: 206,
      headers,
    });
  },
};
