/**
 * Prints a pyramid pattern of '#' and ' ' characters based on the given number.
 *
 * @param {number} n - The number of rows in the pyramid.
 * @return {void} - This function does not return a value.
 */
function pyramid(n) {
  const mid = Math.floor((2 * n - 1) / 2);
  let pyramid = "";
  for (let row = 0; row < n; row++) {
    for (let col = 0; col < 2 * n - 1; col++) {
      if (col >= mid - row && col <= mid + row) {
        pyramid += "#";
      } else {
        pyramid += " ";
      }
    }
    pyramid += "\n";
  }
  console.log(pyramid);
}

pyramid(9);
