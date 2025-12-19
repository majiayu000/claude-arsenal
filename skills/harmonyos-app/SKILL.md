---
name: harmonyos-app
description: HarmonyOS application development expert. Use when building HarmonyOS apps with ArkTS, ArkUI, Stage model, and distributed capabilities. Covers HarmonyOS NEXT (API 12+) best practices.
---
# HarmonyOS Application Development

## Core Principles

- **ArkTS First** — Use ArkTS with strict type safety, no `any` or dynamic types
- **Declarative UI** — Build UI with ArkUI's declarative components and state management
- **Stage Model** — Use modern Stage model (UIAbility), not legacy FA model
- **Distributed by Design** — Leverage cross-device capabilities from the start
- **Atomic Services** — Consider atomic services and cards for lightweight experiences
- **One-time Development** — Design for multi-device adaptation (phone, tablet, watch, TV)

---

## Hard Rules (Must Follow)

> These rules are mandatory. Violating them means the skill is not working correctly.

### No Dynamic Types

**ArkTS prohibits dynamic typing. Never use `any`, type assertions, or dynamic property access.**

```typescript
// ❌ FORBIDDEN: Dynamic types
let data: any = fetchData();
let obj: object = {};
obj['dynamicKey'] = value;  // Dynamic property access
(someVar as SomeType).method();  // Type assertion

// ✅ REQUIRED: Strict typing
interface UserData {
  id: string;
  name: string;
}
let data: UserData = fetchData();

// Use Record for dynamic keys
let obj: Record<string, string> = {};
obj['key'] = value;  // OK with Record type
```

### No Direct State Mutation

**Never mutate @State/@Prop variables directly in nested objects. Use immutable updates.**

```typescript
// ❌ FORBIDDEN: Direct mutation
@State user: User = { name: 'John', age: 25 };

updateAge() {
  this.user.age = 26;  // UI won't update!
}

// ✅ REQUIRED: Immutable update
updateAge() {
  this.user = { ...this.user, age: 26 };  // Creates new object, triggers UI update
}

// For arrays
@State items: string[] = ['a', 'b'];

// ❌ FORBIDDEN
this.items.push('c');  // UI won't update

// ✅ REQUIRED
this.items = [...this.items, 'c'];
```

### Stage Model Only

**Always use Stage model (UIAbility). Never use deprecated FA model (PageAbility).**

```typescript
// ❌ FORBIDDEN: FA Model (deprecated)
// config.json with "pages" array
export default {
  onCreate() { ... }  // PageAbility lifecycle
}

// ✅ REQUIRED: Stage Model
// module.json5 with abilities configuration
import { UIAbility } from '@kit.AbilityKit';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // Modern Stage model lifecycle
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    windowStage.loadContent('pages/Index');
  }
}
```

### Component Reusability

**Extract reusable UI into @Component. No inline complex UI in build() methods.**

```typescript
// ❌ FORBIDDEN: Monolithic build method
@Entry
@Component
struct MainPage {
  build() {
    Column() {
      // 200+ lines of inline UI...
      Row() {
        Image($r('app.media.avatar'))
        Column() {
          Text(this.user.name)
          Text(this.user.email)
        }
      }
      // More inline UI...
    }
  }
}

// ✅ REQUIRED: Extract components
@Component
struct UserCard {
  @Prop user: User;

  build() {
    Row() {
      Image($r('app.media.avatar'))
      Column() {
        Text(this.user.name)
        Text(this.user.email)
      }
    }
  }
}

@Entry
@Component
struct MainPage {
  @State user: User = { name: 'John', email: 'john@example.com' };

  build() {
    Column() {
      UserCard({ user: this.user })
    }
  }
}
```

---

## Quick Reference

### When to Use What

| Scenario | Pattern | Example |
|----------|---------|---------|
| Component-local state | @State | Counter, form inputs |
| Parent-to-child data | @Prop | Read-only child data |
| Two-way binding | @Link | Shared mutable state |
| Cross-component state | @Provide/@Consume | Theme, user context |
| Persistent state | PersistentStorage | User preferences |
| App-wide state | AppStorage | Global state |
| Complex state logic | @Observed/@ObjectLink | Nested object updates |

### State Decorator Selection

```
@State        → Component owns the state, triggers re-render on change
@Prop         → Parent passes value, child gets copy (one-way)
@Link         → Parent passes reference, child can modify (two-way)
@Provide      → Ancestor provides value to all descendants
@Consume      → Descendant consumes value from ancestor
@StorageLink  → Syncs with AppStorage, two-way binding
@StorageProp  → Syncs with AppStorage, one-way binding
@Observed     → Class decorator for observable objects
@ObjectLink   → Links to @Observed object in parent
```

---

## Project Structure

### Recommended Architecture

```
MyApp/
├── entry/                          # Main entry module
│   ├── src/main/
│   │   ├── ets/
│   │   │   ├── entryability/       # UIAbility definitions
│   │   │   │   └── EntryAbility.ets
│   │   │   ├── pages/              # Page components
│   │   │   │   ├── Index.ets
│   │   │   │   └── Detail.ets
│   │   │   ├── components/         # Reusable UI components
│   │   │   │   ├── common/         # Common components
│   │   │   │   └── business/       # Business-specific components
│   │   │   ├── viewmodel/          # ViewModels (MVVM)
│   │   │   ├── model/              # Data models
│   │   │   ├── service/            # Business logic services
│   │   │   ├── repository/         # Data access layer
│   │   │   ├── utils/              # Utility functions
│   │   │   └── constants/          # Constants and configs
│   │   ├── resources/              # Resources (strings, images)
│   │   └── module.json5            # Module configuration
│   └── build-profile.json5
├── common/                         # Shared library module
│   └── src/main/ets/
├── features/                       # Feature modules
│   ├── feature_home/
│   └── feature_profile/
└── build-profile.json5             # Project configuration
```

### Layer Separation

```
┌─────────────────────────────────────┐
│           UI Layer (Pages)          │  ArkUI Components
├─────────────────────────────────────┤
│         ViewModel Layer             │  State management, UI logic
├─────────────────────────────────────┤
│         Service Layer               │  Business logic
├─────────────────────────────────────┤
│        Repository Layer             │  Data access abstraction
├─────────────────────────────────────┤
│    Data Sources (Local/Remote)      │  Preferences, RDB, Network
└─────────────────────────────────────┘
```

---

## ArkUI Component Patterns

### Basic Component Structure

```typescript
import { router } from '@kit.ArkUI';

@Component
export struct ProductCard {
  // Props from parent
  @Prop product: Product;
  @Prop onAddToCart: (product: Product) => void;

  // Local state
  @State isExpanded: boolean = false;

  // Computed values (use getters)
  get formattedPrice(): string {
    return `¥${this.product.price.toFixed(2)}`;
  }

  // Lifecycle
  aboutToAppear(): void {
    console.info('ProductCard appearing');
  }

  aboutToDisappear(): void {
    console.info('ProductCard disappearing');
  }

  // Event handlers
  private handleTap(): void {
    router.pushUrl({ url: 'pages/ProductDetail', params: { id: this.product.id } });
  }

  private handleAddToCart(): void {
    this.onAddToCart(this.product);
  }

  // UI builder
  build() {
    Column() {
      Image(this.product.imageUrl)
        .width('100%')
        .aspectRatio(1)
        .objectFit(ImageFit.Cover)

      Text(this.product.name)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)

      Text(this.formattedPrice)
        .fontSize(14)
        .fontColor('#FF6B00')

      Button('Add to Cart')
        .onClick(() => this.handleAddToCart())
    }
    .padding(12)
    .backgroundColor(Color.White)
    .borderRadius(8)
    .onClick(() => this.handleTap())
  }
}
```

### List with LazyForEach

```typescript
import { BasicDataSource } from '../utils/BasicDataSource';

class ProductDataSource extends BasicDataSource<Product> {
  private products: Product[] = [];

  totalCount(): number {
    return this.products.length;
  }

  getData(index: number): Product {
    return this.products[index];
  }

  addData(product: Product): void {
    this.products.push(product);
    this.notifyDataAdd(this.products.length - 1);
  }

  updateData(index: number, product: Product): void {
    this.products[index] = product;
    this.notifyDataChange(index);
  }
}

@Component
struct ProductList {
  private dataSource: ProductDataSource = new ProductDataSource();

  build() {
    List() {
      LazyForEach(this.dataSource, (product: Product, index: number) => {
        ListItem() {
          ProductCard({ product: product })
        }
      }, (product: Product) => product.id)  // Key generator
    }
    .lanes(2)  // Grid with 2 columns
    .cachedCount(4)  // Cache 4 items for smooth scrolling
  }
}
```

### Custom Dialog

```typescript
@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController;
  title: string = 'Confirm';
  message: string = '';
  onConfirm: () => void = () => {};

  build() {
    Column() {
      Text(this.title)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .margin({ bottom: 16 })

      Text(this.message)
        .fontSize(16)
        .margin({ bottom: 24 })

      Row() {
        Button('Cancel')
          .onClick(() => this.controller.close())
          .backgroundColor(Color.Gray)
          .margin({ right: 16 })

        Button('Confirm')
          .onClick(() => {
            this.onConfirm();
            this.controller.close();
          })
      }
    }
    .padding(24)
  }
}

// Usage
@Entry
@Component
struct MainPage {
  dialogController: CustomDialogController = new CustomDialogController({
    builder: ConfirmDialog({
      title: 'Delete Item',
      message: 'Are you sure you want to delete this item?',
      onConfirm: () => this.deleteItem()
    }),
    autoCancel: true
  });

  private deleteItem(): void {
    // Delete logic
  }

  build() {
    Button('Delete')
      .onClick(() => this.dialogController.open())
  }
}
```

---

## State Management Patterns

### ViewModel Pattern

```typescript
// viewmodel/ProductViewModel.ets
import { Product } from '../model/Product';
import { ProductRepository } from '../repository/ProductRepository';

@Observed
export class ProductViewModel {
  products: Product[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';

  private repository: ProductRepository = new ProductRepository();

  async loadProducts(): Promise<void> {
    this.isLoading = true;
    this.errorMessage = '';

    try {
      this.products = await this.repository.getProducts();
    } catch (error) {
      this.errorMessage = `Failed to load: ${error.message}`;
    } finally {
      this.isLoading = false;
    }
  }

  async addProduct(product: Product): Promise<void> {
    const created = await this.repository.createProduct(product);
    this.products = [...this.products, created];
  }
}

// pages/ProductPage.ets
@Entry
@Component
struct ProductPage {
  @State viewModel: ProductViewModel = new ProductViewModel();

  aboutToAppear(): void {
    this.viewModel.loadProducts();
  }

  build() {
    Column() {
      if (this.viewModel.isLoading) {
        LoadingProgress()
      } else if (this.viewModel.errorMessage) {
        Text(this.viewModel.errorMessage)
          .fontColor(Color.Red)
      } else {
        ForEach(this.viewModel.products, (product: Product) => {
          ProductCard({ product: product })
        }, (product: Product) => product.id)
      }
    }
  }
}
```

### AppStorage for Global State

```typescript
// Initialize in EntryAbility
import { AbilityConstant, UIAbility, Want } from '@kit.AbilityKit';

export default class EntryAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // Initialize global state
    AppStorage.setOrCreate('isLoggedIn', false);
    AppStorage.setOrCreate('currentUser', null);
    AppStorage.setOrCreate('theme', 'light');
  }
}

// Access in components
@Entry
@Component
struct ProfilePage {
  @StorageLink('isLoggedIn') isLoggedIn: boolean = false;
  @StorageLink('currentUser') currentUser: User | null = null;
  @StorageProp('theme') theme: string = 'light';  // Read-only

  build() {
    Column() {
      if (this.isLoggedIn && this.currentUser) {
        Text(`Welcome, ${this.currentUser.name}`)
      } else {
        Button('Login')
          .onClick(() => {
            // After login
            this.isLoggedIn = true;
            this.currentUser = { id: '1', name: 'John' };
          })
      }
    }
  }
}
```

### PersistentStorage for Preferences

```typescript
// Initialize persistent storage
PersistentStorage.persistProp('userSettings', {
  notifications: true,
  darkMode: false,
  language: 'zh-CN'
});

@Entry
@Component
struct SettingsPage {
  @StorageLink('userSettings') settings: UserSettings = {
    notifications: true,
    darkMode: false,
    language: 'zh-CN'
  };

  build() {
    Column() {
      Toggle({ type: ToggleType.Switch, isOn: this.settings.notifications })
        .onChange((isOn: boolean) => {
          this.settings = { ...this.settings, notifications: isOn };
        })

      Toggle({ type: ToggleType.Switch, isOn: this.settings.darkMode })
        .onChange((isOn: boolean) => {
          this.settings = { ...this.settings, darkMode: isOn };
        })
    }
  }
}
```

---

## Navigation Patterns

### Router Navigation

```typescript
import { router } from '@kit.ArkUI';

// Navigate to page
router.pushUrl({
  url: 'pages/Detail',
  params: { productId: '123' }
});

// Navigate with result
router.pushUrl({
  url: 'pages/SelectAddress'
}).then(() => {
  // Navigation complete
});

// Get params in target page
@Entry
@Component
struct DetailPage {
  @State productId: string = '';

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, string>;
    this.productId = params?.productId ?? '';
  }
}

// Go back
router.back();

// Replace current page
router.replaceUrl({ url: 'pages/Home' });

// Clear stack and navigate
router.clear();
router.pushUrl({ url: 'pages/Login' });
```

### Navigation Component (Recommended for HarmonyOS NEXT)

```typescript
@Entry
@Component
struct MainPage {
  @Provide('navPathStack') navPathStack: NavPathStack = new NavPathStack();

  @Builder
  pageBuilder(name: string, params: object) {
    if (name === 'detail') {
      DetailPage({ params: params as DetailParams })
    } else if (name === 'settings') {
      SettingsPage()
    }
  }

  build() {
    Navigation(this.navPathStack) {
      Column() {
        Button('Go to Detail')
          .onClick(() => {
            this.navPathStack.pushPath({ name: 'detail', param: { id: '123' } });
          })
      }
    }
    .navDestination(this.pageBuilder)
    .title('Home')
  }
}

@Component
struct DetailPage {
  @Consume('navPathStack') navPathStack: NavPathStack;
  params: DetailParams = { id: '' };

  build() {
    NavDestination() {
      Column() {
        Text(`Product ID: ${this.params.id}`)
        Button('Back')
          .onClick(() => this.navPathStack.pop())
      }
    }
    .title('Detail')
  }
}
```

---

## Network Requests

### HTTP Client

```typescript
import { http } from '@kit.NetworkKit';

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

class HttpClient {
  private baseUrl: string = 'https://api.example.com';

  async get<T>(path: string): Promise<T> {
    const httpRequest = http.createHttp();

    try {
      const response = await httpRequest.request(
        `${this.baseUrl}${path}`,
        {
          method: http.RequestMethod.GET,
          header: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${await this.getToken()}`
          },
          expectDataType: http.HttpDataType.OBJECT
        }
      );

      if (response.responseCode === 200) {
        const result = response.result as ApiResponse<T>;
        if (result.code === 0) {
          return result.data;
        }
        throw new Error(result.message);
      }
      throw new Error(`HTTP ${response.responseCode}`);
    } finally {
      httpRequest.destroy();
    }
  }

  async post<T, R>(path: string, data: T): Promise<R> {
    const httpRequest = http.createHttp();

    try {
      const response = await httpRequest.request(
        `${this.baseUrl}${path}`,
        {
          method: http.RequestMethod.POST,
          header: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${await this.getToken()}`
          },
          extraData: JSON.stringify(data),
          expectDataType: http.HttpDataType.OBJECT
        }
      );

      const result = response.result as ApiResponse<R>;
      return result.data;
    } finally {
      httpRequest.destroy();
    }
  }

  private async getToken(): Promise<string> {
    return AppStorage.get('authToken') ?? '';
  }
}

export const httpClient = new HttpClient();
```

---

## Distributed Capabilities

### Cross-Device Data Sync

```typescript
import { distributedKVStore } from '@kit.ArkData';

class DistributedStore {
  private kvManager: distributedKVStore.KVManager | null = null;
  private kvStore: distributedKVStore.SingleKVStore | null = null;

  async init(context: Context): Promise<void> {
    const config: distributedKVStore.KVManagerConfig = {
      context: context,
      bundleName: 'com.example.myapp'
    };

    this.kvManager = distributedKVStore.createKVManager(config);

    const options: distributedKVStore.Options = {
      createIfMissing: true,
      encrypt: false,
      backup: false,
      autoSync: true,  // Auto sync across devices
      kvStoreType: distributedKVStore.KVStoreType.SINGLE_VERSION,
      securityLevel: distributedKVStore.SecurityLevel.S1
    };

    this.kvStore = await this.kvManager.getKVStore('myStore', options);
  }

  async put(key: string, value: string): Promise<void> {
    await this.kvStore?.put(key, value);
  }

  async get(key: string): Promise<string | null> {
    try {
      return await this.kvStore?.get(key) as string;
    } catch {
      return null;
    }
  }

  // Subscribe to changes from other devices
  subscribe(callback: (key: string, value: string) => void): void {
    this.kvStore?.on('dataChange', distributedKVStore.SubscribeType.SUBSCRIBE_TYPE_ALL,
      (data: distributedKVStore.ChangeNotification) => {
        for (const entry of data.insertEntries) {
          callback(entry.key, entry.value.value as string);
        }
        for (const entry of data.updateEntries) {
          callback(entry.key, entry.value.value as string);
        }
      }
    );
  }
}
```

### Device Discovery and Connection

```typescript
import { distributedDeviceManager } from '@kit.DistributedServiceKit';

class DeviceManager {
  private deviceManager: distributedDeviceManager.DeviceManager | null = null;

  async init(context: Context): Promise<void> {
    this.deviceManager = distributedDeviceManager.createDeviceManager(
      context.applicationInfo.name
    );
  }

  getAvailableDevices(): distributedDeviceManager.DeviceBasicInfo[] {
    return this.deviceManager?.getAvailableDeviceListSync() ?? [];
  }

  startDiscovery(): void {
    const filter: distributedDeviceManager.DiscoveryFilter = {
      discoverMode: distributedDeviceManager.DiscoverMode.DISCOVER_MODE_PASSIVE
    };

    this.deviceManager?.startDiscovering(filter);

    this.deviceManager?.on('discoverSuccess', (data) => {
      console.info(`Found device: ${data.device.deviceName}`);
    });
  }

  stopDiscovery(): void {
    this.deviceManager?.stopDiscovering();
  }
}
```

---

## Multi-Device Adaptation

### Responsive Layout

```typescript
import { BreakpointSystem, BreakPointType } from '../utils/BreakpointSystem';

@Entry
@Component
struct AdaptivePage {
  @StorageProp('currentBreakpoint') currentBreakpoint: string = 'sm';

  build() {
    GridRow({
      columns: { sm: 4, md: 8, lg: 12 },
      gutter: { x: 12, y: 12 }
    }) {
      GridCol({ span: { sm: 4, md: 4, lg: 3 } }) {
        // Sidebar - full width on phone, 1/3 on tablet, 1/4 on desktop
        Sidebar()
      }

      GridCol({ span: { sm: 4, md: 4, lg: 9 } }) {
        // Content - full width on phone, 2/3 on tablet, 3/4 on desktop
        MainContent()
      }
    }
  }
}

// Breakpoint system
export class BreakpointSystem {
  private static readonly BREAKPOINTS: Record<string, number> = {
    'sm': 320,   // Phone
    'md': 600,   // Foldable/Tablet
    'lg': 840    // Desktop/TV
  };

  static register(context: UIContext): void {
    context.getMediaQuery().matchMediaSync('(width >= 840vp)').on('change', (result) => {
      AppStorage.setOrCreate('currentBreakpoint', result.matches ? 'lg' : 'md');
    });

    context.getMediaQuery().matchMediaSync('(width >= 600vp)').on('change', (result) => {
      if (!result.matches) {
        AppStorage.setOrCreate('currentBreakpoint', 'sm');
      }
    });
  }
}
```

---

## Testing

### Unit Testing

```typescript
import { describe, it, expect, beforeEach } from '@ohos/hypium';
import { ProductViewModel } from '../viewmodel/ProductViewModel';

export default function ProductViewModelTest() {
  describe('ProductViewModel', () => {
    let viewModel: ProductViewModel;

    beforeEach(() => {
      viewModel = new ProductViewModel();
    });

    it('should load products successfully', async () => {
      await viewModel.loadProducts();

      expect(viewModel.products.length).assertLarger(0);
      expect(viewModel.isLoading).assertFalse();
      expect(viewModel.errorMessage).assertEqual('');
    });

    it('should add product to list', async () => {
      const initialCount = viewModel.products.length;
      const newProduct: Product = { id: 'test', name: 'Test Product', price: 99 };

      await viewModel.addProduct(newProduct);

      expect(viewModel.products.length).assertEqual(initialCount + 1);
    });
  });
}
```

### UI Testing

```typescript
import { describe, it, expect } from '@ohos/hypium';
import { Driver, ON } from '@ohos.UiTest';

export default function ProductPageUITest() {
  describe('ProductPage UI', () => {
    it('should display product list', async () => {
      const driver = Driver.create();
      await driver.delayMs(1000);

      // Find and verify list exists
      const list = await driver.findComponent(ON.type('List'));
      expect(list).not().assertNull();

      // Verify list items
      const items = await driver.findComponents(ON.type('ListItem'));
      expect(items.length).assertLarger(0);
    });

    it('should navigate to detail on tap', async () => {
      const driver = Driver.create();

      // Find first product card
      const card = await driver.findComponent(ON.type('ProductCard'));
      await card.click();

      await driver.delayMs(500);

      // Verify navigation to detail page
      const detailTitle = await driver.findComponent(ON.text('Product Detail'));
      expect(detailTitle).not().assertNull();
    });
  });
}
```

---

## Checklist

```markdown
## Project Setup
- [ ] Stage model used (not FA model)
- [ ] module.json5 properly configured
- [ ] Permissions declared in module.json5
- [ ] Resource files organized (strings, images)

## Code Quality
- [ ] No `any` types in codebase
- [ ] All state decorated with proper decorators
- [ ] No direct mutation of @State objects
- [ ] Components extracted for reusability
- [ ] Lifecycle methods used appropriately

## UI/UX
- [ ] LazyForEach used for long lists
- [ ] Loading states implemented
- [ ] Error handling with user feedback
- [ ] Multi-device layouts with GridRow/GridCol
- [ ] Accessibility attributes added

## State Management
- [ ] Clear state ownership (component vs global)
- [ ] @Observed/@ObjectLink for nested objects
- [ ] PersistentStorage for user preferences
- [ ] AppStorage for app-wide state

## Performance
- [ ] Images optimized and cached
- [ ] Unnecessary re-renders avoided
- [ ] Network requests with proper error handling
- [ ] Background tasks properly managed

## Testing
- [ ] Unit tests for ViewModels
- [ ] UI tests for critical flows
- [ ] Edge cases covered
```

---

## See Also

- [reference/arkts.md](reference/arkts.md) — ArkTS language guide and restrictions
- [reference/arkui.md](reference/arkui.md) — ArkUI components and styling
- [reference/stage-model.md](reference/stage-model.md) — Stage model architecture
- [reference/distributed.md](reference/distributed.md) — Distributed capabilities guide
- [templates/project-structure.md](templates/project-structure.md) — Project template
