/**
 * reverse int by js functions
 * @param {Number} n
 * @returns
 */
function reverseInt(n) {
  const reversed = n.toString().split("").reverse().join("");
  return parseInt(reversed) * Math.sign(n);
}

console.log(reverseInt(-15));

/**
 * reverse string by js function
 * @param {string} str
 * @returns
 */
function reverse(str) {
  return str.split("").reverse().join("");
}

console.log(reverse("Coding"));

/**
 * reverse string manually
 * @param {string} str
 * @returns
 */
function reverse(str) {
  let reversed = "";

  for (let char of str) {
    reversed = char + reversed;
  }

  return reversed;
}

console.log(reverse("Coding"));
