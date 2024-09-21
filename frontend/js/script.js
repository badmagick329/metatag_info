const form = document.querySelector(".url-form");
const urlInput = document.querySelector(".url-input");
const selectedTagsInput = document.querySelector(".selected-tags-input");
const outputText = document.querySelector(".output-text");
const submitButton = document.querySelector(".submit-button");

/**
 * @param {FormDataEvent} e
 */
async function handleSubmit(e) {
  e.preventDefault();
  const url = cleanedURL(urlInput.value);
  try {
    submitButton.setAttribute("disabled", true);
    const response = await fetch("/url", {
      method: "POST",
      body: JSON.stringify({
        url,
        selected_tags: splitTags(selectedTagsInput.value),
      }),
      headers: { "Content-Type": "application/json" },
    });
    const parsed = await response.json();
    const data = parsed.data;
    const error = parsed.error;
    outputText.textContent = data === null ? error : data;
  } catch (e) {
    console.error(e);
    outputText.textContent = `An error occurred\n${e}`;
  } finally {
    submitButton.removeAttribute("disabled");
  }
}

/**
 * @param {string} url
 * @returns {string}
 */
function cleanedURL(url) {
  url = url.trim();
  if (!(url.startsWith("https://") || url.startsWith("http://"))) {
    url = `https://${url}`;
  }
  return url;
}

/**
 * @param {string|null} tags_text
 * @returns {string[]}
 */
function splitTags(tags_text) {
  if (typeof tags_text !== "string") {
    return [];
  }
  tags_text = tags_text.trim();
  if (tags_text === "") {
    return [];
  }
  return tags_text.split(",");
}

function main() {
  submitButton.addEventListener("click", handleSubmit);
}

main();
