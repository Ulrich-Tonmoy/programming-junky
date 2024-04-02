# Welcome To Lodasher 😎

This is a coding exercise for getting a firm grasp on JavaScript fundamentals.

**implemented** some methods from a popular library called "Lodash".

## Tip 1: Run A Specific Test

The `jest` command accepts a filter string as its argument, which tells jest to only run test file patterns that match your filter string.

For example, you can run just the "map" test by:

```sh
npm test -- map
#        ^^ These extra hyphens tells `npm` to relay everything after
#           the double hyphen to the underlying `jest` command.
```

## Tip 2: Run Jest under "watch" mode

You can run Jest in "watch" mode, which gets it to watch our source code and re-run the test automatically.

You can do this using the `-w` or `--watch` flag:

```sh
npm test -- --watch
npm test -- --watchAll # (For those of you running this in replit.com)
```

## Tip 3: Disable certain tests

You can disable certain tests or blocks of tests in the source code by changing any `describe`, `test`, or `it` statements to `xdescribe`, `xtest`, or `xit`:

```javascript
xdescribe("foobar", function () {
  // Nothing here will run.
  it("should not run", function () {
    /* ... */
  });
  it("should not run either", function () {
    /* ... */
  });
});

describe("bizbaz", function () {
  it("should run", function () {
    // This test will run.
  });

  xit("should not run", function () {
    // This test will not run.
  });
});
```

# Reference / Docs

- [Lodash](https://lodash.com/)
- [Jest](https://jestjs.io/)
