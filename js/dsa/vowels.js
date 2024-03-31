/**
 * Count the number of vowels in a given string.
 * manual check
 * @param {string} str - the input string to count vowels from
 * @return {number} the count of vowels in the input string
 */
function vowels(str) {
  const vowelCheck = ["a", "e", "i", "o", "u"];

  let count = 0;

  for (let char of str.toLowerCase()) {
    if (vowelCheck.includes(char)) count++;
  }

  return count;
}

console.log(vowels("Coding"));

/**
 * Returns the number of vowels in a given string.
 * Using Regex
 * @param {string} str - the input string
 * @return {number} the number of vowels in the input string
 */
function vowels(str) {
  const matches = str.match(/[aeiou]/gi);
  return matches ? matches.length : 0;
}

console.log(vowels("Coding"));
