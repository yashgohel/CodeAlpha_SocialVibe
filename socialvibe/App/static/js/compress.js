// Image compression helper to prevent 413 Payload Too Large on Vercel
function compressImage(file, maxDimension, quality) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = function (event) {
      const img = new Image();
      img.onload = function () {
        const canvas = document.createElement('canvas');
        let width = img.width;
        let height = img.height;

        // Calculate new dimensions keeping aspect ratio
        if (width > height) {
          if (width > maxDimension) {
            height = Math.round((height * maxDimension) / width);
            width = maxDimension;
          }
        } else {
          if (height > maxDimension) {
            width = Math.round((width * maxDimension) / height);
            height = maxDimension;
          }
        }

        canvas.width = width;
        canvas.height = height;

        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, width, height);

        canvas.toBlob(
          (blob) => {
            const compressedFile = new File([blob], file.name, {
              type: 'image/jpeg',
              lastModified: Date.now(),
            });
            resolve(compressedFile);
          },
          'image/jpeg',
          quality
        );
      };
      img.src = event.target.result;
    };
    reader.readAsDataURL(file);
  });
}

document.addEventListener('change', async (event) => {
  if (event.target.tagName === 'INPUT' && event.target.type === 'file') {
    const input = event.target;
    if (!input.files || input.files.length === 0) return;

    if (input.dataset.compressing === 'true') return;

    const files = Array.from(input.files);
    const dataTransfer = new DataTransfer();
    let hasChanged = false;

    for (const file of files) {
      // Only compress images that are larger than 1MB (1,048,576 bytes)
      if (file.type.startsWith('image/') && file.size > 1024 * 1024) {
        hasChanged = true;
        input.dataset.compressing = 'true';
        
        // Show status cursor
        document.body.style.cursor = 'wait';
        
        const compressed = await compressImage(file, 1200, 0.8);
        dataTransfer.items.add(compressed);
        
        document.body.style.cursor = 'default';
      } else {
        dataTransfer.items.add(file);
      }
    }

    if (hasChanged) {
      input.files = dataTransfer.files;
      // Trigger a change event so previews or other listeners update with the new compressed file
      input.dispatchEvent(new Event('change', { bubbles: true }));
    }
    input.removeAttribute('data-compressing');
  }
});
