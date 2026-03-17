export interface VideoSegment {
    id: string;
    startTime: number;
    endTime: number;
    image: string;
}

export interface ExportOptions {
    title: string;
    audioSrc: string;
    segments: VideoSegment[];
    onProgress?: (progress: number) => void;
}

/**
 * @author antigravity
 * Advanced video exporter that combines lesson illustrations and audio into an MP4/WebM file.
 * Features:
 * - Dynamic MIME type detection for maximum compatibility (H.264/MP4 preferred).
 * - "Sticky image" logic to prevent black screens during audio gaps.
 * - Real-time progress reporting.
 */
export async function exportToMp4(options: ExportOptions): Promise<Blob> {
    const { audioSrc, segments, onProgress } = options;
    const width = 1280;
    const height = 720;

    // 1. Initialize Canvas
    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d', { alpha: false })!;

    // 2. Prepare Audio
    const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
    const response = await fetch(audioSrc);
    const arrayBuffer = await response.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
    const duration = audioBuffer.duration;

    // 3. Setup Media Recorder
    const getSupportedMimeType = () => {
        const types = [
            'video/mp4;codecs=avc1,mp4a.40.2',
            'video/mp4;codecs=avc1',
            'video/webm;codecs=vp9,opus',
            'video/webm;codecs=vp8,vorbis',
            'video/webm'
        ];
        return types.find(type => MediaRecorder.isTypeSupported(type)) || 'video/webm';
    };

    const mimeType = getSupportedMimeType();
    const stream = canvas.captureStream(30); // 30 FPS

    // Create audio stream from buffer
    const mediaStreamDestination = audioContext.createMediaStreamDestination();
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(mediaStreamDestination);
    source.connect(audioContext.destination);

    // Combine canvas and audio streams
    const combinedStream = new MediaStream([
        ...stream.getVideoTracks(),
        ...mediaStreamDestination.stream.getAudioTracks()
    ]);

    const recorder = new MediaRecorder(combinedStream, { mimeType });

    const chunks: Blob[] = [];
    recorder.ondataavailable = (e) => chunks.push(e.data);

    return new Promise(async (resolve, reject) => {
        recorder.onstop = () => {
            const blob = new Blob(chunks, { type: mimeType });
            resolve(blob);
        };

        recorder.onerror = (e) => reject(e);

        // 4. Preload Images
        const imageCache: Map<string, HTMLImageElement> = new Map();
        const uniqueImages = Array.from(new Set(segments.map(s => s.image)));

        await Promise.all(uniqueImages.map(url => {
            return new Promise((resolveImg) => {
                const img = new Image();
                img.crossOrigin = 'anonymous';
                img.onload = () => {
                    imageCache.set(url, img);
                    resolveImg(null);
                };
                img.onerror = () => {
                    console.error('Failed to load image:', url);
                    resolveImg(null);
                };
                img.src = url;
            });
        }));

        // 5. Start Recording
        recorder.start();
        source.start();

        const startTime = performance.now();
        let lastImg: HTMLImageElement | null = null;

        const renderFrame = () => {
            const elapsed = (performance.now() - startTime) / 1000;

            if (elapsed >= duration) {
                recorder.stop();
                source.stop();
                audioContext.close();
                return;
            }

            // Find current segment
            const currentSegment = segments.find(s => elapsed >= s.startTime && elapsed <= s.endTime);
            let img = currentSegment ? imageCache.get(currentSegment.image) : null;

            // If no segment matches current time, use the previous image (prevent black screen)
            if (!img && lastImg) {
                img = lastImg;
            }

            // Draw image
            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, width, height);

            if (img) {
                const scale = Math.max(width / img.width, height / img.height);
                const x = (width - img.width * scale) / 2;
                const y = (height - img.height * scale) / 2;
                ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
                lastImg = img;
            }

            if (onProgress) {
                onProgress(Math.min(100, (elapsed / duration) * 100));
            }

            requestAnimationFrame(renderFrame);
        };

        requestAnimationFrame(renderFrame);
    });
}
