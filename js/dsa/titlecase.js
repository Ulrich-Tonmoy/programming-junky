/**
 * Capitalizes the first letter of each word in a given string.
 *
 * @param {string} str - The input string to capitalize.
 * @return {string} The capitalized string.
 */
function capitalize(str) {
  const words = str.split(" ");

  return words.map((word) => word[0].toUpperCase() + word.slice(1)).join(" ");
}

console.log(capitalize("this is coding in javaScript"));
