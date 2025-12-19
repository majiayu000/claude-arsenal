# ArkTS Language Guide

ArkTS is a TypeScript superset optimized for HarmonyOS with static typing enforcement and UI declaration extensions.

## Key Differences from TypeScript

### Prohibited Features

```typescript
// ❌ These TypeScript features are NOT allowed in ArkTS

// 1. any type
let data: any;  // Error!

// 2. unknown type with assertions
let value: unknown;
(value as string).length;  // Error!

// 3. Dynamic property access
let obj = {};
obj['key'] = value;  // Error! (unless Record type)

// 4. Structural typing for classes
class A { x: number = 0; }
class B { x: number = 0; }
let a: A = new B();  // Error! Classes must be explicitly related

// 5. typeof for types
type T = typeof someVariable;  // Error!

// 6. keyof operator
type Keys = keyof SomeType;  // Error!

// 7. Indexed access types
type Value = SomeType['key'];  // Error!

// 8. Conditional types
type Check<T> = T extends string ? 'yes' : 'no';  // Error!

// 9. Mapped types
type Readonly<T> = { readonly [P in keyof T]: T[P] };  // Error!

// 10. Symbol and unique symbol
const sym = Symbol('key');  // Error!
```

### Allowed Patterns

```typescript
// ✅ These patterns are supported

// 1. Explicit types
let data: string = 'hello';
let count: number = 42;

// 2. Interfaces
interface User {
  id: string;
  name: string;
  age?: number;  // Optional properties OK
}

// 3. Type aliases (basic)
type UserId = string;
type Callback = (data: string) => void;

// 4. Generics (basic)
class Container<T> {
  private value: T;

  constructor(value: T) {
    this.value = value;
  }

  getValue(): T {
    return this.value;
  }
}

// 5. Union types (basic)
type Status = 'loading' | 'success' | 'error';
let status: Status = 'loading';

// 6. Record type for dynamic keys
let map: Record<string, number> = {};
map['key1'] = 100;  // OK with Record

// 7. Enums
enum Color {
  Red,
  Green,
  Blue
}

// 8. Class inheritance
class Animal {
  name: string = '';
}

class Dog extends Animal {
  breed: string = '';
}
```

## Type System

### Primitive Types

```typescript
// Numbers
let integer: number = 42;
let float: number = 3.14;

// Strings
let text: string = 'Hello';
let template: string = `Value: ${integer}`;

// Booleans
let flag: boolean = true;

// Arrays
let numbers: number[] = [1, 2, 3];
let strings: Array<string> = ['a', 'b', 'c'];

// Tuples
let tuple: [string, number] = ['age', 25];

// Null and undefined
let nullable: string | null = null;
let optional: string | undefined = undefined;
```

### Object Types

```typescript
// Interface
interface Product {
  readonly id: string;  // Read-only
  name: string;
  price: number;
  description?: string;  // Optional
}

// Implementation
const product: Product = {
  id: 'prod_001',
  name: 'Phone',
  price: 999
};

// Type alias
type Point = {
  x: number;
  y: number;
};
```

### Function Types

```typescript
// Function declarations
function add(a: number, b: number): number {
  return a + b;
}

// Arrow functions
const multiply = (a: number, b: number): number => a * b;

// Optional parameters
function greet(name: string, greeting?: string): string {
  return `${greeting ?? 'Hello'}, ${name}`;
}

// Default parameters
function createUser(name: string, role: string = 'user'): User {
  return { name, role };
}

// Rest parameters
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}

// Callback types
type ClickHandler = (event: ClickEvent) => void;

function setOnClick(handler: ClickHandler): void {
  // ...
}
```

### Generics

```typescript
// Generic function
function identity<T>(value: T): T {
  return value;
}

// Generic interface
interface Repository<T> {
  getById(id: string): Promise<T>;
  save(item: T): Promise<void>;
  delete(id: string): Promise<void>;
}

// Generic class
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }
}

// Generic constraints (basic)
interface HasId {
  id: string;
}

class EntityRepository<T extends HasId> {
  private entities: Map<string, T> = new Map();

  save(entity: T): void {
    this.entities.set(entity.id, entity);
  }
}
```

## Classes

### Class Declaration

```typescript
class User {
  // Properties with default values (required in ArkTS)
  private id: string = '';
  public name: string = '';
  protected email: string = '';
  readonly createdAt: Date = new Date();

  // Static members
  static userCount: number = 0;

  // Constructor
  constructor(id: string, name: string, email: string) {
    this.id = id;
    this.name = name;
    this.email = email;
    User.userCount++;
  }

  // Methods
  public getDisplayName(): string {
    return this.name;
  }

  private validateEmail(): boolean {
    return this.email.includes('@');
  }

  // Getter/Setter
  get displayId(): string {
    return `USER-${this.id}`;
  }

  set displayId(value: string) {
    this.id = value.replace('USER-', '');
  }

  // Static method
  static createGuest(): User {
    return new User('guest', 'Guest', 'guest@example.com');
  }
}
```

### Inheritance

```typescript
// Base class
abstract class Shape {
  abstract area(): number;
  abstract perimeter(): number;

  describe(): string {
    return `Area: ${this.area()}, Perimeter: ${this.perimeter()}`;
  }
}

// Derived class
class Rectangle extends Shape {
  constructor(private width: number, private height: number) {
    super();
  }

  area(): number {
    return this.width * this.height;
  }

  perimeter(): number {
    return 2 * (this.width + this.height);
  }
}

// Interface implementation
interface Drawable {
  draw(): void;
}

class Circle extends Shape implements Drawable {
  constructor(private radius: number) {
    super();
  }

  area(): number {
    return Math.PI * this.radius ** 2;
  }

  perimeter(): number {
    return 2 * Math.PI * this.radius;
  }

  draw(): void {
    console.info(`Drawing circle with radius ${this.radius}`);
  }
}
```

## Async/Await

```typescript
// Async function
async function fetchUser(id: string): Promise<User> {
  const response = await httpClient.get<User>(`/users/${id}`);
  return response;
}

// Error handling
async function safeGetUser(id: string): Promise<User | null> {
  try {
    return await fetchUser(id);
  } catch (error) {
    console.error(`Failed to fetch user: ${(error as Error).message}`);
    return null;
  }
}

// Parallel execution
async function loadDashboard(): Promise<DashboardData> {
  const [user, orders, notifications] = await Promise.all([
    fetchUser('current'),
    fetchOrders(),
    fetchNotifications()
  ]);

  return { user, orders, notifications };
}

// Sequential execution
async function processOrders(orderIds: string[]): Promise<void> {
  for (const id of orderIds) {
    await processOrder(id);  // One at a time
  }
}
```

## Module System

```typescript
// Named exports
// utils/math.ets
export function add(a: number, b: number): number {
  return a + b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}

export const PI = 3.14159;

// Default export
// models/User.ets
export default class User {
  constructor(public name: string) {}
}

// Named imports
import { add, multiply, PI } from '../utils/math';

// Default import
import User from '../models/User';

// Rename imports
import { add as sum } from '../utils/math';

// Import all
import * as MathUtils from '../utils/math';
MathUtils.add(1, 2);

// Re-export
// index.ets
export { add, multiply } from './math';
export { default as User } from './User';
```

## Best Practices

### 1. Always Initialize Properties

```typescript
// ❌ Bad
class User {
  name: string;  // Error: not initialized
}

// ✅ Good
class User {
  name: string = '';
}

// ✅ Also good: initialize in constructor
class User {
  name: string;
  constructor(name: string) {
    this.name = name;
  }
}
```

### 2. Use Explicit Return Types

```typescript
// ❌ Bad
function getUser(id: string) {
  return { id, name: 'John' };
}

// ✅ Good
function getUser(id: string): User {
  return { id, name: 'John' };
}
```

### 3. Prefer Interfaces Over Type Aliases for Objects

```typescript
// ✅ Preferred for object types
interface User {
  id: string;
  name: string;
}

// Use type for unions, primitives, tuples
type Status = 'active' | 'inactive';
type Coordinate = [number, number];
```

### 4. Use Record for Dynamic Keys

```typescript
// ❌ Bad
let cache = {};
cache['key'] = value;  // Error!

// ✅ Good
let cache: Record<string, CacheEntry> = {};
cache['key'] = value;  // OK
```

### 5. Avoid Optional Chaining on Non-Nullable

```typescript
// ❌ Bad: unnecessary optional chaining
const user: User = getUser();
console.log(user?.name);  // user is not nullable

// ✅ Good
console.log(user.name);
```
