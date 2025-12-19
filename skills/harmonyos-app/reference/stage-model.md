# Stage Model Architecture

Stage Model is the application model for HarmonyOS 3.1+, providing structured lifecycle management and component-based architecture.

## Core Concepts

### Application Components

```
┌─────────────────────────────────────────────────────┐
│                    AbilityStage                      │
│  (Application-level lifecycle, shared resources)     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────┐  │
│  │  UIAbility   │  │  UIAbility   │  │ Extension │  │
│  │  (Page 1)    │  │  (Page 2)    │  │ Ability   │  │
│  └──────────────┘  └──────────────┘  └───────────┘  │
│                                                      │
└─────────────────────────────────────────────────────┘
```

| Component | Purpose | Example |
|-----------|---------|---------|
| AbilityStage | Application entry, global lifecycle | Initialize app, load resources |
| UIAbility | UI page container | Main page, settings page |
| ExtensionAbility | Background services | Widget, notification, share |
| WindowStage | Window management | Multi-window, split screen |

## AbilityStage

### Implementation

```typescript
// entry/src/main/ets/AbilityStage.ets
import { AbilityStage, Want } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

export default class MyAbilityStage extends AbilityStage {
  onCreate(): void {
    // Called when application starts
    hilog.info(0x0000, 'AbilityStage', 'onCreate');

    // Initialize global resources
    this.initializeApp();
  }

  onAcceptWant(want: Want): string {
    // Handle incoming want
    // Return ability name to launch
    if (want.action === 'share') {
      return 'ShareAbility';
    }
    return 'MainAbility';
  }

  private initializeApp(): void {
    // Initialize services, database, etc.
  }
}
```

### Configuration

```json
// module.json5
{
  "module": {
    "name": "entry",
    "type": "entry",
    "srcEntry": "./ets/AbilityStage.ets",
    "abilities": [
      {
        "name": "MainAbility",
        "srcEntry": "./ets/abilities/MainAbility.ets",
        "launchType": "singleton",
        "exported": true
      }
    ]
  }
}
```

## UIAbility

### Lifecycle

```
┌─────────────────────────────────────────────────────┐
│                    UIAbility Lifecycle               │
├─────────────────────────────────────────────────────┤
│                                                      │
│  onCreate() ──► onWindowStageCreate() ──► onForeground()
│       │                  │                    │
│       │                  │                    ▼
│       │                  │              (User Interaction)
│       │                  │                    │
│       │                  │                    ▼
│  onDestroy() ◄── onWindowStageDestroy() ◄── onBackground()
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Implementation

```typescript
// entry/src/main/ets/abilities/MainAbility.ets
import { UIAbility, AbilityConstant, Want } from '@kit.AbilityKit';
import { window } from '@kit.ArkUI';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG = 'MainAbility';

export default class MainAbility extends UIAbility {
  private windowStage: window.WindowStage | null = null;

  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    hilog.info(0x0000, TAG, 'onCreate');

    // Handle launch parameters
    const action = want.action;
    const uri = want.uri;

    if (action === 'deeplink') {
      this.handleDeepLink(uri);
    }
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    hilog.info(0x0000, TAG, 'onWindowStageCreate');

    this.windowStage = windowStage;

    // Load main page
    windowStage.loadContent('pages/Index', (err) => {
      if (err.code) {
        hilog.error(0x0000, TAG, 'Failed to load content: %{public}s', JSON.stringify(err));
        return;
      }
      hilog.info(0x0000, TAG, 'Content loaded successfully');
    });

    // Configure window
    this.configureWindow(windowStage);
  }

  onForeground(): void {
    hilog.info(0x0000, TAG, 'onForeground');
    // App enters foreground
    // Resume tasks, refresh data
  }

  onBackground(): void {
    hilog.info(0x0000, TAG, 'onBackground');
    // App enters background
    // Save state, pause non-critical tasks
  }

  onWindowStageDestroy(): void {
    hilog.info(0x0000, TAG, 'onWindowStageDestroy');
    // Release UI resources
  }

  onDestroy(): void {
    hilog.info(0x0000, TAG, 'onDestroy');
    // Cleanup resources
  }

  onNewWant(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // Called when singleton ability receives new launch request
    hilog.info(0x0000, TAG, 'onNewWant');
    this.handleIntent(want);
  }

  private configureWindow(windowStage: window.WindowStage): void {
    const win = windowStage.getMainWindowSync();

    // Set status bar
    win.setWindowLayoutFullScreen(true);
    win.setWindowSystemBarEnable(['status', 'navigation']);

    // Set colors
    const sysBarProps: window.SystemBarProperties = {
      statusBarColor: '#FFFFFF',
      navigationBarColor: '#FFFFFF',
      statusBarContentColor: '#000000'
    };
    win.setWindowSystemBarProperties(sysBarProps);
  }

  private handleDeepLink(uri: string | undefined): void {
    if (!uri) return;
    // Parse and handle deep link
  }

  private handleIntent(want: Want): void {
    // Handle intent routing
  }
}
```

## Launch Types

### Singleton (Default)

```json
// module.json5
{
  "abilities": [{
    "name": "MainAbility",
    "launchType": "singleton"
  }]
}
```

- Only one instance exists
- `onNewWant()` called for subsequent launches
- Suitable for main entry, settings

### Standard

```json
{
  "abilities": [{
    "name": "DetailAbility",
    "launchType": "standard"
  }]
}
```

- New instance for each launch
- Multiple instances can exist
- Suitable for detail pages, editors

### Specified

```json
{
  "abilities": [{
    "name": "DocumentAbility",
    "launchType": "specified"
  }]
}
```

- Instance determined by key
- Same key reuses instance
- Suitable for document editing

```typescript
// Launching specified ability
const want: Want = {
  bundleName: 'com.example.app',
  abilityName: 'DocumentAbility',
  parameters: {
    'instanceKey': 'document_123'
  }
};
```

## Page Navigation

### Router Navigation

```typescript
import { router } from '@kit.ArkUI';

// Navigate to page
router.pushUrl({
  url: 'pages/Detail',
  params: {
    id: '123',
    title: 'Product Detail'
  }
});

// Replace current page
router.replaceUrl({
  url: 'pages/Login'
});

// Go back
router.back();

// Go back with result
router.back({
  url: 'pages/List',
  params: { refresh: true }
});

// Clear and navigate
router.clear();
router.pushUrl({ url: 'pages/Home' });
```

### Receiving Parameters

```typescript
import { router } from '@kit.ArkUI';

@Entry
@Component
struct DetailPage {
  @State id: string = '';
  @State title: string = '';

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, string>;
    this.id = params?.id ?? '';
    this.title = params?.title ?? '';
  }

  build() {
    Column() {
      Text(this.title)
      // Page content
    }
  }
}
```

### Navigation Component

```typescript
import { Navigation, NavPathStack } from '@kit.ArkUI';

@Entry
@Component
struct MainPage {
  @Provide('navStack') navStack: NavPathStack = new NavPathStack();

  build() {
    Navigation(this.navStack) {
      // Root content
      HomeContent()
    }
    .navDestination(this.PageBuilder)
    .mode(NavigationMode.Stack)
  }

  @Builder
  PageBuilder(name: string, params: Object): void {
    if (name === 'detail') {
      DetailPage({ params: params as DetailParams })
    } else if (name === 'settings') {
      SettingsPage()
    }
  }
}

@Component
struct HomeContent {
  @Consume('navStack') navStack: NavPathStack;

  build() {
    Column() {
      Button('Go to Detail')
        .onClick(() => {
          this.navStack.pushPath({
            name: 'detail',
            param: { id: '123' }
          });
        })
    }
  }
}
```

## Context Usage

### Getting Context

```typescript
import { common, UIAbility } from '@kit.AbilityKit';

// In UIAbility
class MyAbility extends UIAbility {
  onCreate(): void {
    const context = this.context;
    // Use context
  }
}

// In Component (via getContext)
@Component
struct MyComponent {
  private context = getContext(this) as common.UIAbilityContext;

  aboutToAppear(): void {
    // Access context
    const filesDir = this.context.filesDir;
  }
}
```

### Context Capabilities

```typescript
import { common } from '@kit.AbilityKit';

@Component
struct ContextDemo {
  private context = getContext(this) as common.UIAbilityContext;

  // File paths
  getFilePaths(): void {
    const filesDir = this.context.filesDir;      // App files
    const cacheDir = this.context.cacheDir;      // Cache
    const tempDir = this.context.tempDir;        // Temporary
    const databaseDir = this.context.databaseDir; // Database
  }

  // Start another ability
  async startAbility(): Promise<void> {
    const want: Want = {
      bundleName: 'com.example.target',
      abilityName: 'TargetAbility'
    };

    await this.context.startAbility(want);
  }

  // Start ability for result
  async startForResult(): Promise<void> {
    const want: Want = {
      bundleName: 'com.example.picker',
      abilityName: 'ImagePickerAbility'
    };

    const result = await this.context.startAbilityForResult(want);
    if (result.resultCode === 0) {
      const imageUri = result.want?.uri;
    }
  }

  // Terminate self
  terminateSelf(): void {
    this.context.terminateSelf();
  }

  // Terminate with result
  terminateWithResult(): void {
    const result: common.AbilityResult = {
      resultCode: 0,
      want: {
        parameters: { selectedId: '123' }
      }
    };
    this.context.terminateSelfWithResult(result);
  }
}
```

## Extension Abilities

### Widget Extension

```typescript
// entry/src/main/ets/formability/FormAbility.ets
import { FormExtensionAbility, formBindingData, formInfo } from '@kit.FormKit';

export default class FormAbility extends FormExtensionAbility {
  onAddForm(want: Want): formBindingData.FormBindingData {
    const formData: Record<string, string> = {
      'title': 'Widget Title',
      'content': 'Widget Content'
    };
    return formBindingData.createFormBindingData(formData);
  }

  onUpdateForm(formId: string): void {
    // Update widget data
    const formData: Record<string, string> = {
      'title': 'Updated Title'
    };
    const bindingData = formBindingData.createFormBindingData(formData);
    formProvider.updateForm(formId, bindingData);
  }

  onRemoveForm(formId: string): void {
    // Cleanup when widget removed
  }
}
```

### Service Extension

```typescript
// For background tasks
import { ServiceExtensionAbility, Want } from '@kit.AbilityKit';

export default class BackgroundService extends ServiceExtensionAbility {
  onCreate(want: Want): void {
    // Initialize service
  }

  onRequest(want: Want, startId: number): void {
    // Handle service request
  }

  onDestroy(): void {
    // Cleanup
  }
}
```

## State Persistence

### Preferences

```typescript
import { preferences } from '@kit.ArkData';
import { common } from '@kit.AbilityKit';

class PreferencesManager {
  private prefs: preferences.Preferences | null = null;
  private context: common.UIAbilityContext;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }

  async init(): Promise<void> {
    this.prefs = await preferences.getPreferences(this.context, 'app_prefs');
  }

  async set(key: string, value: preferences.ValueType): Promise<void> {
    if (!this.prefs) return;
    await this.prefs.put(key, value);
    await this.prefs.flush();
  }

  async get<T extends preferences.ValueType>(key: string, defaultValue: T): Promise<T> {
    if (!this.prefs) return defaultValue;
    return await this.prefs.get(key, defaultValue) as T;
  }

  async remove(key: string): Promise<void> {
    if (!this.prefs) return;
    await this.prefs.delete(key);
    await this.prefs.flush();
  }
}
```

### Application State

```typescript
// Using AppStorage for app-wide state
AppStorage.setOrCreate('isLoggedIn', false);
AppStorage.setOrCreate('userId', '');

// Access in components
@Component
struct ProfilePage {
  @StorageLink('isLoggedIn') isLoggedIn: boolean = false;
  @StorageLink('userId') userId: string = '';

  build() {
    Column() {
      if (this.isLoggedIn) {
        Text(`User: ${this.userId}`)
      } else {
        Text('Please login')
      }
    }
  }
}

// Persist to disk
PersistentStorage.persistProp('isLoggedIn', false);
PersistentStorage.persistProp('userId', '');
```

## Best Practices

### Lifecycle Management

```typescript
// ✅ Good: Proper lifecycle handling
export default class MainAbility extends UIAbility {
  onCreate(): void {
    // Initialize only essential resources
  }

  onWindowStageCreate(windowStage: window.WindowStage): void {
    // Load UI, initialize view-related resources
  }

  onForeground(): void {
    // Resume operations, refresh data
    this.refreshData();
  }

  onBackground(): void {
    // Pause operations, save state
    this.saveState();
    this.pauseNonCriticalTasks();
  }

  onDestroy(): void {
    // Full cleanup
    this.releaseResources();
  }
}
```

### Memory Management

```typescript
// ✅ Good: Release resources properly
@Component
struct ResourceAwarePage {
  private subscription: Subscription | null = null;

  aboutToAppear(): void {
    this.subscription = eventBus.subscribe('event', this.handleEvent);
  }

  aboutToDisappear(): void {
    // Always unsubscribe
    this.subscription?.unsubscribe();
    this.subscription = null;
  }

  handleEvent = (data: EventData): void => {
    // Handle event
  }
}
```

### Navigation Patterns

```typescript
// ✅ Good: Use NavPathStack for complex navigation
@Entry
@Component
struct App {
  @Provide('navStack') navStack: NavPathStack = new NavPathStack();

  build() {
    Navigation(this.navStack) {
      // Content
    }
    .navDestination(this.routeBuilder)
  }

  @Builder
  routeBuilder(name: string): void {
    // Centralized route handling
  }
}

// ❌ Bad: Direct router calls scattered everywhere
// Hard to track navigation flow, no type safety
```
