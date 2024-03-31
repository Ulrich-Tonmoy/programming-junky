/**
 * Generates a staircase pattern of "#" and " " characters with a given number of steps.
 *
 * @param {number} n - The number of steps in the staircase.
 * @return {undefined} - This function does not return a value.
 */
function steps(n) {
  let steps = "";
  for (let row = 1; row <= n; row++) {
    for (let col = 1; col <= n; col++) {
      if (col <= row) {
        steps += "#";
      }
    }
    steps += "\n";
  }
  console.log(steps);
}

steps(6);
