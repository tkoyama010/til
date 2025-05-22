// hello.ts
function greet(name: string): string {
  return `Hello, ${name.toUpperCase()}!`;
}

const user = "Tetsuo";
console.log(greet(user));
