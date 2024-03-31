/**
 * Returns the character that appears most frequently in the given string.
 *
 * @param {string} str - The input string.
 * @return {string} The character that appears most frequently in the string.
 */
function maxChar(str) {
  const charObj = {};

  for (let char of str) {
    charObj[char] = ++charObj[char] || 1;
  }

  let max = 0;
  let maxChar = "";
  for (let key in charObj) {
    if (charObj[key] > max) {
      max = charObj[key];
      maxChar = key;
    }
  }

  return maxChar;
}

console.log(maxChar("apple 1231111"));
