/**
 * Check if the input string is a palindrome.
 *
 * @param {string} str - The input string to check
 * @return {boolean} Returns true if the input string is a palindrome, false otherwise
 */
function palindrome(str) {
  const reversed = str.split("").reverse().join("");

  return str === reversed;
}

console.log(palindrome("coding"));
