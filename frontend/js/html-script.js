const form = document.querySelector(".url-form");
const htmlInput = document.querySelector(".html-input");
const outputText = document.querySelector(".output-text");
const submitButton = document.querySelector(".submit-button");

/**
 * @param {FormDataEvent} e
 */
async function handleSubmit(e) {
  e.preventDefault();
  try {
    submitButton.setAttribute("disabled", true);
    const response = await fetch("/convert", {
      method: "POST",
      body: JSON.stringify({ html: htmlInput.value }),
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

function main() {
  submitButton.addEventListener("click", handleSubmit);
}

main();
