/**
 * Splits an array into chunks of a specified size.
 *
 * @param {Array} array - The array to be split into chunks.
 * @param {number} size - The size of each chunk.
 * @return {Array} An array of chunks, where each chunk is a subarray of the original array.
 */
function chunk(array, size) {
  const result = [];
  let index = 0;
  while (index < array.length) {
    result.push(array.slice(index, index + size));
    index += size;
  }
  return result;
}

console.log(chunk([1, 2, 3, 4, 5, 6, 7, 8], 3));
