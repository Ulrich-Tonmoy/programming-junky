/**
 * A function that prints "fizz" for multiples of 3, "buzz" for multiples of 5,
 * "fizzbuzz" for multiples of both, and the number for all other cases up to n.
 * @param {number} n - the number to iterate up to
 * @return {undefined} This function does not return a value
 */
function fizzBuzz(n) {
  for (let i = 1; i <= n; i++) {
    if (i % 3 === 0 && i % 5 === 0) {
      console.log("fizzbuzz");
    } else if (i % 3 === 0) {
      console.log("fizz");
    } else if (i % 5 === 0) {
      console.log("buzz");
    } else {
      console.log(i);
    }
  }
}

fizzBuzz(20);
