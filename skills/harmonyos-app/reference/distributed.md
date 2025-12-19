# Distributed Capabilities

HarmonyOS distributed capabilities enable seamless collaboration between devices in a Super Device ecosystem.

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Super Device Ecosystem                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Phone   │◄──►│  Tablet  │◄──►│  Watch   │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲              ▲                                       │
│       │              │                                       │
│       ▼              ▼                                       │
│  ┌──────────┐    ┌──────────┐                              │
│  │    TV    │◄──►│   Car    │                              │
│  └──────────┘    └──────────┘                              │
│                                                              │
│  Capabilities:                                               │
│  • Distributed Data    • Cross-device Call                  │
│  • Distributed Objects • Device Discovery                   │
│  • Distributed Files   • Ability Continuation               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Device Discovery

### Discovering Nearby Devices

```typescript
import { distributedDeviceManager } from '@kit.DistributedServiceKit';

class DeviceDiscovery {
  private deviceManager: distributedDeviceManager.DeviceManager | null = null;

  async init(): Promise<void> {
    this.deviceManager = distributedDeviceManager.createDeviceManager('com.example.app');
  }

  // Get trusted devices (already authenticated)
  getTrustedDevices(): distributedDeviceManager.DeviceBasicInfo[] {
    if (!this.deviceManager) return [];
    return this.deviceManager.getAvailableDeviceListSync();
  }

  // Start discovery
  startDiscovery(): void {
    if (!this.deviceManager) return;

    const discoverParam: distributedDeviceManager.DiscoveryParam = {
      discoverTargetType: distributedDeviceManager.DiscoverTargetType.DEVICE
    };

    this.deviceManager.startDiscovering(discoverParam);

    this.deviceManager.on('discoverSuccess', (data) => {
      console.info(`Discovered device: ${data.device.deviceName}`);
    });

    this.deviceManager.on('discoverFailure', (reason) => {
      console.error(`Discovery failed: ${reason}`);
    });
  }

  // Stop discovery
  stopDiscovery(): void {
    this.deviceManager?.stopDiscovering();
  }

  // Authenticate device
  async authenticateDevice(device: distributedDeviceManager.DeviceBasicInfo): Promise<void> {
    if (!this.deviceManager) return;

    const authParam: distributedDeviceManager.AuthParam = {
      authType: distributedDeviceManager.AuthType.PIN_CODE,
      extraInfo: {}
    };

    await this.deviceManager.authenticateDevice(device, authParam);
  }

  release(): void {
    this.deviceManager?.release();
    this.deviceManager = null;
  }
}
```

### Device Selection UI

```typescript
@Component
struct DeviceSelector {
  @State devices: distributedDeviceManager.DeviceBasicInfo[] = [];
  @State selectedDevice: distributedDeviceManager.DeviceBasicInfo | null = null;
  private discovery: DeviceDiscovery = new DeviceDiscovery();

  async aboutToAppear(): Promise<void> {
    await this.discovery.init();
    this.devices = this.discovery.getTrustedDevices();
  }

  aboutToDisappear(): void {
    this.discovery.release();
  }

  build() {
    Column() {
      Text('Select Device')
        .fontSize(20)
        .fontWeight(FontWeight.Bold)

      List() {
        ForEach(this.devices, (device: distributedDeviceManager.DeviceBasicInfo) => {
          ListItem() {
            Row() {
              Image(this.getDeviceIcon(device.deviceType))
                .width(32)
                .height(32)
              Text(device.deviceName)
                .margin({ left: 12 })
              Blank()
              if (this.selectedDevice?.deviceId === device.deviceId) {
                Image($r('app.media.check'))
              }
            }
            .width('100%')
            .padding(16)
            .onClick(() => {
              this.selectedDevice = device;
            })
          }
        })
      }
    }
  }

  getDeviceIcon(type: distributedDeviceManager.DeviceType): Resource {
    switch (type) {
      case distributedDeviceManager.DeviceType.PHONE:
        return $r('app.media.phone');
      case distributedDeviceManager.DeviceType.TABLET:
        return $r('app.media.tablet');
      case distributedDeviceManager.DeviceType.TV:
        return $r('app.media.tv');
      default:
        return $r('app.media.device');
    }
  }
}
```

## Distributed Data

### Distributed KV Store

```typescript
import { distributedKVStore } from '@kit.ArkData';

class DistributedStorage {
  private kvManager: distributedKVStore.KVManager | null = null;
  private kvStore: distributedKVStore.SingleKVStore | null = null;

  async init(context: common.UIAbilityContext): Promise<void> {
    const config: distributedKVStore.KVManagerConfig = {
      bundleName: 'com.example.app',
      context: context
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

    this.kvStore = await this.kvManager.getKVStore('shared_store', options);
  }

  // Put data
  async put(key: string, value: string | number | boolean): Promise<void> {
    await this.kvStore?.put(key, value);
  }

  // Get data
  async get(key: string): Promise<string | number | boolean | null> {
    try {
      return await this.kvStore?.get(key);
    } catch {
      return null;
    }
  }

  // Delete data
  async delete(key: string): Promise<void> {
    await this.kvStore?.delete(key);
  }

  // Subscribe to changes
  subscribeToChanges(callback: (changes: distributedKVStore.ChangeNotification) => void): void {
    this.kvStore?.on('dataChange', distributedKVStore.SubscribeType.SUBSCRIBE_TYPE_ALL, callback);
  }

  // Manual sync
  async sync(deviceIds: string[]): Promise<void> {
    await this.kvStore?.sync(deviceIds, distributedKVStore.SyncMode.PUSH_PULL);
  }

  close(): void {
    this.kvManager?.closeKVStore('shared_store');
  }
}
```

### Usage in Component

```typescript
@Component
struct SyncedNotes {
  @State notes: string = '';
  private storage: DistributedStorage = new DistributedStorage();

  async aboutToAppear(): Promise<void> {
    const context = getContext(this) as common.UIAbilityContext;
    await this.storage.init(context);

    // Load existing notes
    const savedNotes = await this.storage.get('notes');
    if (savedNotes) {
      this.notes = savedNotes as string;
    }

    // Subscribe to changes from other devices
    this.storage.subscribeToChanges((changes) => {
      for (const entry of changes.insertEntries) {
        if (entry.key === 'notes') {
          this.notes = entry.value.value as string;
        }
      }
      for (const entry of changes.updateEntries) {
        if (entry.key === 'notes') {
          this.notes = entry.value.value as string;
        }
      }
    });
  }

  build() {
    Column() {
      TextArea({ text: this.notes })
        .width('100%')
        .height(300)
        .onChange((value: string) => {
          this.notes = value;
          this.storage.put('notes', value);
        })

      Text('Changes sync automatically to all devices')
        .fontSize(12)
        .fontColor('#888888')
    }
  }
}
```

## Distributed Objects

### Creating Distributed Object

```typescript
import { distributedDataObject } from '@kit.ArkData';

interface GameState {
  score: number;
  level: number;
  playerPosition: { x: number; y: number };
}

class DistributedGameState {
  private dataObject: distributedDataObject.DataObject | null = null;
  private state: GameState = {
    score: 0,
    level: 1,
    playerPosition: { x: 0, y: 0 }
  };

  async init(context: common.UIAbilityContext): Promise<void> {
    this.dataObject = distributedDataObject.create(context, this.state);

    // Set session ID for sync
    await this.dataObject.setSessionId('game_session_001');

    // Watch for changes
    this.dataObject.on('change', (sessionId: string, fields: string[]) => {
      console.info(`Fields changed: ${fields.join(', ')}`);
      this.onStateChanged(fields);
    });

    this.dataObject.on('status', (sessionId: string, networkId: string, status: string) => {
      console.info(`Sync status: ${status}`);
    });
  }

  updateScore(score: number): void {
    if (this.dataObject) {
      (this.dataObject as Object)['score'] = score;
    }
  }

  updatePosition(x: number, y: number): void {
    if (this.dataObject) {
      (this.dataObject as Object)['playerPosition'] = { x, y };
    }
  }

  private onStateChanged(fields: string[]): void {
    // Handle state changes from other devices
  }

  async leave(): Promise<void> {
    await this.dataObject?.setSessionId('');
  }
}
```

## Cross-Device Call

### Starting Remote Ability

```typescript
import { common, Want } from '@kit.AbilityKit';

class RemoteAbilityLauncher {
  private context: common.UIAbilityContext;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }

  // Start ability on remote device
  async startRemoteAbility(deviceId: string): Promise<void> {
    const want: Want = {
      deviceId: deviceId,
      bundleName: 'com.example.app',
      abilityName: 'PlayerAbility',
      parameters: {
        videoUrl: 'https://example.com/video.mp4',
        startPosition: 120
      }
    };

    await this.context.startAbility(want);
  }

  // Start and get result from remote device
  async startRemoteForResult(deviceId: string): Promise<common.AbilityResult> {
    const want: Want = {
      deviceId: deviceId,
      bundleName: 'com.example.picker',
      abilityName: 'FilePickerAbility'
    };

    return await this.context.startAbilityForResult(want);
  }

  // Connect to remote service
  async connectRemoteService(deviceId: string): Promise<void> {
    const want: Want = {
      deviceId: deviceId,
      bundleName: 'com.example.app',
      abilityName: 'ComputeService'
    };

    const connection: common.ConnectOptions = {
      onConnect: (elementName, remoteProxy) => {
        console.info('Connected to remote service');
        // Use remoteProxy to call remote methods
      },
      onDisconnect: (elementName) => {
        console.info('Disconnected from remote service');
      },
      onFailed: (code) => {
        console.error(`Connection failed: ${code}`);
      }
    };

    const connectionId = this.context.connectServiceExtensionAbility(want, connection);
  }
}
```

### Multi-Screen Collaboration

```typescript
@Component
struct MultiScreenApp {
  @State isRemoteDisplayActive: boolean = false;
  private context = getContext(this) as common.UIAbilityContext;

  build() {
    Column() {
      if (this.isRemoteDisplayActive) {
        // Controller UI (on phone)
        this.ControllerView()
      } else {
        // Full content (on this device)
        this.ContentView()
      }

      Button('Cast to TV')
        .onClick(() => this.castToTV())
    }
  }

  @Builder
  ControllerView() {
    Column() {
      Text('Playing on TV')
      Row() {
        Button('◀')
        Button('⏸')
        Button('▶')
      }
    }
  }

  @Builder
  ContentView() {
    // Video player content
  }

  async castToTV(): Promise<void> {
    // Get TV device
    const deviceManager = distributedDeviceManager.createDeviceManager('com.example.app');
    const devices = deviceManager.getAvailableDeviceListSync();
    const tvDevice = devices.find(d =>
      d.deviceType === distributedDeviceManager.DeviceType.TV
    );

    if (tvDevice) {
      const want: Want = {
        deviceId: tvDevice.deviceId,
        bundleName: 'com.example.app',
        abilityName: 'PlayerAbility',
        parameters: {
          videoUrl: this.currentVideoUrl
        }
      };

      await this.context.startAbility(want);
      this.isRemoteDisplayActive = true;
    }
  }
}
```

## Ability Continuation

### Enabling Continuation

```typescript
// MainAbility.ets
import { UIAbility, AbilityConstant, Want } from '@kit.AbilityKit';

export default class MainAbility extends UIAbility {
  onCreate(want: Want, launchParam: AbilityConstant.LaunchParam): void {
    // Check if this is a continuation
    if (launchParam.launchReason === AbilityConstant.LaunchReason.CONTINUATION) {
      // Restore state from continuation
      this.restoreFromContinuation(want);
    }
  }

  // Prepare data for continuation
  onContinue(wantParam: Record<string, Object>): AbilityConstant.OnContinueResult {
    // Save current state
    wantParam['currentPage'] = 'detail';
    wantParam['articleId'] = '123';
    wantParam['scrollPosition'] = 450;

    return AbilityConstant.OnContinueResult.AGREE;
  }

  private restoreFromContinuation(want: Want): void {
    const params = want.parameters;
    if (params) {
      const currentPage = params['currentPage'] as string;
      const articleId = params['articleId'] as string;
      const scrollPosition = params['scrollPosition'] as number;

      // Navigate to saved state
      router.pushUrl({
        url: `pages/${currentPage}`,
        params: { id: articleId, scroll: scrollPosition }
      });
    }
  }
}
```

### Configuration

```json
// module.json5
{
  "module": {
    "abilities": [{
      "name": "MainAbility",
      "continuable": true,
      "launchType": "singleton"
    }]
  }
}
```

### Triggering Continuation

```typescript
@Component
struct ContinuationDemo {
  private context = getContext(this) as common.UIAbilityContext;

  async continueToDevice(deviceId: string): Promise<void> {
    // Continuation will trigger onContinue callback
    await this.context.continueAbility({
      deviceId: deviceId,
      bundleName: 'com.example.app',
      abilityName: 'MainAbility'
    });
  }

  build() {
    Button('Continue on Tablet')
      .onClick(async () => {
        const devices = await this.getAvailableDevices();
        const tablet = devices.find(d =>
          d.deviceType === distributedDeviceManager.DeviceType.TABLET
        );
        if (tablet) {
          await this.continueToDevice(tablet.deviceId);
        }
      })
  }
}
```

## Distributed File System

### Sharing Files Across Devices

```typescript
import { fileIo } from '@kit.CoreFileKit';
import { common } from '@kit.AbilityKit';

class DistributedFileManager {
  private context: common.UIAbilityContext;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }

  // Get distributed file path
  getDistributedPath(relativePath: string): string {
    return `${this.context.distributedFilesDir}/${relativePath}`;
  }

  // Write file (will sync to other devices)
  async writeDistributedFile(relativePath: string, content: string): Promise<void> {
    const filePath = this.getDistributedPath(relativePath);
    const file = fileIo.openSync(filePath, fileIo.OpenMode.READ_WRITE | fileIo.OpenMode.CREATE);

    try {
      fileIo.writeSync(file.fd, content);
    } finally {
      fileIo.closeSync(file);
    }
  }

  // Read file (may come from another device)
  async readDistributedFile(relativePath: string): Promise<string> {
    const filePath = this.getDistributedPath(relativePath);
    const file = fileIo.openSync(filePath, fileIo.OpenMode.READ_ONLY);

    try {
      const stat = fileIo.statSync(filePath);
      const buffer = new ArrayBuffer(stat.size);
      fileIo.readSync(file.fd, buffer);
      return String.fromCharCode(...new Uint8Array(buffer));
    } finally {
      fileIo.closeSync(file);
    }
  }

  // List distributed files
  listDistributedFiles(): string[] {
    const dir = this.context.distributedFilesDir;
    return fileIo.listFileSync(dir);
  }
}
```

## Best Practices

### Security Considerations

```typescript
// ✅ Good: Validate device trust before sharing sensitive data
async shareData(deviceId: string, data: SensitiveData): Promise<void> {
  const device = this.getTrustedDevice(deviceId);

  if (!device) {
    throw new Error('Device not trusted');
  }

  // Only share with authenticated devices
  if (device.authForm === distributedDeviceManager.AuthForm.IDENTICAL_ACCOUNT) {
    await this.secureShare(deviceId, data);
  }
}

// ✅ Good: Use appropriate security level
const options: distributedKVStore.Options = {
  securityLevel: distributedKVStore.SecurityLevel.S3,  // High security
  encrypt: true  // Encrypt data
};
```

### Error Handling

```typescript
// ✅ Good: Handle network and device errors gracefully
async startRemoteAbility(deviceId: string): Promise<void> {
  try {
    await this.context.startAbility(want);
  } catch (err) {
    const error = err as BusinessError;

    switch (error.code) {
      case 16000050:
        // Device offline
        this.showToast('Device is not available');
        break;
      case 16000051:
        // Network error
        this.showToast('Network connection failed');
        break;
      case 16000001:
        // Ability not found
        this.showToast('App not installed on target device');
        break;
      default:
        this.showToast('Failed to connect to device');
    }
  }
}
```

### Performance

```typescript
// ✅ Good: Batch updates for distributed objects
updateGameState(updates: Partial<GameState>): void {
  // Batch multiple changes
  const dataObject = this.dataObject as Object;

  Object.entries(updates).forEach(([key, value]) => {
    dataObject[key] = value;
  });

  // Changes will be synced together
}

// ✅ Good: Use appropriate sync modes
async syncData(urgent: boolean): Promise<void> {
  if (urgent) {
    // Push immediately
    await this.kvStore.sync(deviceIds, distributedKVStore.SyncMode.PUSH);
  } else {
    // Let system decide when to sync
    await this.kvStore.sync(deviceIds, distributedKVStore.SyncMode.PUSH_PULL);
  }
}
```

### State Management

```typescript
// ✅ Good: Handle continuation state properly
@Component
struct ContinuableComponent {
  @State articleContent: string = '';
  @State scrollOffset: number = 0;

  // Save state for continuation
  getContinuationState(): Record<string, Object> {
    return {
      'articleContent': this.articleContent,
      'scrollOffset': this.scrollOffset
    };
  }

  // Restore state after continuation
  restoreContinuationState(state: Record<string, Object>): void {
    this.articleContent = state['articleContent'] as string;
    this.scrollOffset = state['scrollOffset'] as number;
  }
}
```

## Common Patterns

### Device Handoff

```typescript
// Phone to tablet handoff for video watching
class VideoHandoff {
  async handoffToTablet(): Promise<void> {
    const currentPosition = this.videoPlayer.getCurrentPosition();
    const videoUrl = this.videoPlayer.getVideoUrl();

    // Find tablet
    const tablet = await this.findTablet();
    if (!tablet) return;

    // Start player on tablet with current position
    const want: Want = {
      deviceId: tablet.deviceId,
      bundleName: 'com.example.video',
      abilityName: 'PlayerAbility',
      parameters: {
        videoUrl: videoUrl,
        startPosition: currentPosition
      }
    };

    await this.context.startAbility(want);

    // Pause local playback
    this.videoPlayer.pause();
  }
}
```

### Collaborative Editing

```typescript
// Real-time document collaboration
class CollaborativeDocument {
  private distributedObject: distributedDataObject.DataObject;

  async init(): Promise<void> {
    const document = {
      content: '',
      lastEditor: '',
      version: 0
    };

    this.distributedObject = distributedDataObject.create(this.context, document);
    await this.distributedObject.setSessionId('doc_session');

    this.distributedObject.on('change', (_, fields) => {
      if (fields.includes('content')) {
        this.onContentChanged();
      }
    });
  }

  updateContent(content: string, editor: string): void {
    const doc = this.distributedObject as Object;
    doc['content'] = content;
    doc['lastEditor'] = editor;
    doc['version'] = (doc['version'] as number) + 1;
  }

  private onContentChanged(): void {
    // Update UI with new content
    const doc = this.distributedObject as Object;
    this.refreshContent(doc['content'] as string);
  }
}
```
