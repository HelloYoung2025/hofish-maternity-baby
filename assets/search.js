const filter = document.querySelector("#filter");
const entries = [...document.querySelectorAll("#results .cards > li")];
const empty = document.querySelector("#no-results");

function searchable(text) {
  return text.normalize("NFD").replace(/\p{M}/gu, "").toLocaleLowerCase();
}

const descriptions = entries.map((entry) => searchable(entry.textContent));
filter.parentElement.hidden = false;
filter.addEventListener("input", () => {
  const words = searchable(filter.value.trim()).split(/\s+/);
  let matches = 0;
  entries.forEach((entry, index) => {
    const visible = words.every((word) => descriptions[index].includes(word));
    entry.hidden = !visible;
    matches += Number(visible);
  });
  empty.hidden = matches !== 0;
});
