/**
 * Cleans the input string by converting it to lowercase, removing non-word characters,
 * sorting the characters, and joining them back together.
 *
 * @param {string} str - the input string to be cleaned
 * @return {string} the cleaned string
 */
function cleanStr(str) {
  return str.toLowerCase().replace(/[\W]/g, "").split("").sort().join("");
}
/**
 * Checks if two strings are anagrams of each other.
 *
 * @param {string} stringA - The first string to compare.
 * @param {string} stringB - The second string to compare.
 * @return {boolean} Returns true if the strings are anagrams, false otherwise.
 */
function anagrams(stringA, stringB) {
  return cleanStr(stringA) === cleanStr(stringB);
}

console.log(anagrams("RAIL! SAFETY!", "fairy tales"));

// ---------------------------------------------------------------------------------------

/**
 * Generates a character map of the input string, counting the frequency of each character.
 *
 * @param {string} str - The input string to generate the character map from.
 * @return {object} An object representing the character map with characters as keys and their frequencies as values.
 */
function charMap(str) {
  const charMap = {};
  str = str.toLowerCase().replace(/[\W]/g, "");
  for (let char of str) {
    charMap[char] = ++charMap[char] || 1;
  }
  return charMap;
}

/**
 * Checks if two strings are anagrams of each other.
 *
 * @param {string} stringA - The first string to check.
 * @param {string} stringB - The second string to check.
 * @return {boolean} Returns true if the strings are anagrams, false otherwise.
 */
function anagrams(stringA, stringB) {
  const charMapA = charMap(stringA);

  const charMapB = charMap(stringB);

  if (Object.keys(charMapA).length !== Object.keys(charMapB).length) return false;

  for (let key in charMapA) {
    if (charMapA[key] !== charMapB[key]) return false;
  }

  return true;
}

console.log(anagrams("RAIL! SAFETY!", "fairy tales"));
