(function () {
  const imageSelector = [
    ".article-body img:not([data-no-lightbox]):not(.no-lightbox)",
    ".photo-page figure img:not([data-no-lightbox]):not(.no-lightbox)",
  ].join(", ");

  const images = Array.from(document.querySelectorAll(imageSelector)).filter((image) => {
    return image.currentSrc || image.src;
  });

  if (!images.length) {
    return;
  }

  let currentIndex = 0;

  const lightbox = document.createElement("div");
  lightbox.className = "image-lightbox";
  lightbox.hidden = true;
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");

  lightbox.innerHTML = [
    '<button class="image-lightbox-close" type="button" aria-label="关闭">×</button>',
    '<button class="image-lightbox-control image-lightbox-prev" type="button" aria-label="上一张">‹</button>',
    '<figure class="image-lightbox-frame">',
    '  <img class="image-lightbox-image" alt="">',
    '  <figcaption class="image-lightbox-caption"></figcaption>',
    '</figure>',
    '<button class="image-lightbox-control image-lightbox-next" type="button" aria-label="下一张">›</button>',
  ].join("");

  document.body.appendChild(lightbox);

  const closeButton = lightbox.querySelector(".image-lightbox-close");
  const prevButton = lightbox.querySelector(".image-lightbox-prev");
  const nextButton = lightbox.querySelector(".image-lightbox-next");
  const lightboxImage = lightbox.querySelector(".image-lightbox-image");
  const caption = lightbox.querySelector(".image-lightbox-caption");

  function getCaption(image) {
    const figure = image.closest("figure");
    const figureCaption = figure ? figure.querySelector("figcaption") : null;
    if (figureCaption && figureCaption.textContent.trim()) {
      return figureCaption.textContent.trim();
    }
    return image.alt || "";
  }

  function showImage(index) {
    currentIndex = (index + images.length) % images.length;
    const image = images[currentIndex];
    lightboxImage.src = image.currentSrc || image.src;
    lightboxImage.alt = image.alt || "";

    const captionText = getCaption(image);
    caption.textContent = captionText;
    caption.hidden = !captionText;

    const hasMultipleImages = images.length > 1;
    prevButton.hidden = !hasMultipleImages;
    nextButton.hidden = !hasMultipleImages;
  }

  function openLightbox(index) {
    showImage(index);
    lightbox.hidden = false;
    document.documentElement.classList.add("lightbox-open");
    closeButton.focus({ preventScroll: true });
  }

  function closeLightbox() {
    lightbox.hidden = true;
    lightboxImage.removeAttribute("src");
    document.documentElement.classList.remove("lightbox-open");
  }

  function showPrevious() {
    showImage(currentIndex - 1);
  }

  function showNext() {
    showImage(currentIndex + 1);
  }

  images.forEach((image, index) => {
    image.classList.add("lightbox-enabled");
    image.addEventListener("click", (event) => {
      event.preventDefault();
      openLightbox(index);
    });
  });

  closeButton.addEventListener("click", closeLightbox);
  prevButton.addEventListener("click", showPrevious);
  nextButton.addEventListener("click", showNext);

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox || event.target === lightboxImage) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (lightbox.hidden) {
      return;
    }
    if (event.key === "Escape") {
      closeLightbox();
    }
    if (event.key === "ArrowLeft" && images.length > 1) {
      showPrevious();
    }
    if (event.key === "ArrowRight" && images.length > 1) {
      showNext();
    }
  });
})();
