# ArkUI Component Guide

ArkUI is the declarative UI framework for HarmonyOS applications.

## Component Basics

### Built-in Components

```typescript
// Text
Text('Hello World')
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#333333')

// Image
Image($r('app.media.icon'))
  .width(100)
  .height(100)
  .objectFit(ImageFit.Cover)

// Button
Button('Click Me')
  .type(ButtonType.Capsule)
  .width(200)
  .height(48)
  .onClick(() => {
    console.info('Button clicked');
  })

// TextInput
TextInput({ placeholder: 'Enter text' })
  .width('100%')
  .height(48)
  .onChange((value: string) => {
    this.inputValue = value;
  })
```

### Layout Containers

```typescript
// Column - Vertical layout
Column() {
  Text('Item 1')
  Text('Item 2')
  Text('Item 3')
}
.width('100%')
.alignItems(HorizontalAlign.Center)
.justifyContent(FlexAlign.SpaceBetween)

// Row - Horizontal layout
Row() {
  Image($r('app.media.avatar')).width(48).height(48)
  Text('Username').margin({ left: 12 })
  Blank()  // Flexible space
  Image($r('app.media.arrow'))
}
.width('100%')
.padding(16)

// Stack - Overlapping layout
Stack({ alignContent: Alignment.BottomEnd }) {
  Image($r('app.media.photo'))
  Badge({ count: 5 })
}

// Flex - Flexible layout
Flex({
  direction: FlexDirection.Row,
  wrap: FlexWrap.Wrap,
  justifyContent: FlexAlign.SpaceAround
}) {
  ForEach(this.items, (item: Item) => {
    ItemCard({ item: item })
  })
}
```

### List Components

```typescript
// Basic List
List() {
  ForEach(this.dataList, (item: DataItem, index: number) => {
    ListItem() {
      Text(item.name)
    }
  }, (item: DataItem) => item.id)
}
.width('100%')
.divider({ strokeWidth: 1, color: '#E8E8E8' })

// Swipe Actions
List() {
  ForEach(this.items, (item: Item) => {
    ListItem() {
      ItemRow({ item: item })
    }
    .swipeAction({
      end: this.DeleteButton(item.id)
    })
  })
}

@Builder
DeleteButton(id: string) {
  Button('Delete')
    .backgroundColor(Color.Red)
    .onClick(() => this.deleteItem(id))
}

// Grid
Grid() {
  ForEach(this.products, (product: Product) => {
    GridItem() {
      ProductCard({ product: product })
    }
  })
}
.columnsTemplate('1fr 1fr')  // 2 columns
.rowsGap(12)
.columnsGap(12)

// WaterFlow (Masonry layout)
WaterFlow() {
  ForEach(this.images, (image: ImageData) => {
    FlowItem() {
      Image(image.url)
        .width('100%')
        .aspectRatio(image.aspectRatio)
    }
  })
}
.columnsTemplate('1fr 1fr')
```

### Scroll Components

```typescript
// Scroll
Scroll() {
  Column() {
    ForEach(this.items, (item: Item) => {
      ItemCard({ item: item })
    })
  }
}
.scrollable(ScrollDirection.Vertical)
.scrollBar(BarState.Auto)
.edgeEffect(EdgeEffect.Spring)

// Swiper
Swiper() {
  ForEach(this.banners, (banner: Banner) => {
    Image(banner.imageUrl)
      .width('100%')
      .height(200)
  })
}
.autoPlay(true)
.interval(3000)
.indicator(true)

// Tabs
Tabs({ barPosition: BarPosition.Start }) {
  TabContent() {
    HomeTab()
  }.tabBar('Home')

  TabContent() {
    DiscoverTab()
  }.tabBar('Discover')

  TabContent() {
    ProfileTab()
  }.tabBar('Profile')
}
.barMode(BarMode.Fixed)
.onChange((index: number) => {
  this.currentTab = index;
})
```

## Custom Components

### Basic Structure

```typescript
@Component
struct UserCard {
  // Props from parent
  @Prop username: string = '';
  @Prop avatarUrl: string = '';

  // Local state
  @State isFollowing: boolean = false;

  build() {
    Row() {
      Image(this.avatarUrl)
        .width(48)
        .height(48)
        .borderRadius(24)

      Column() {
        Text(this.username)
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
      }
      .margin({ left: 12 })
      .alignItems(HorizontalAlign.Start)

      Blank()

      Button(this.isFollowing ? 'Following' : 'Follow')
        .onClick(() => {
          this.isFollowing = !this.isFollowing;
        })
    }
    .width('100%')
    .padding(16)
  }
}
```

### @Builder Functions

```typescript
@Component
struct ProductList {
  @State products: Product[] = [];

  // Private builder
  @Builder
  ProductItem(product: Product) {
    Row() {
      Image(product.imageUrl)
        .width(80)
        .height(80)
      Column() {
        Text(product.name)
        Text(`$${product.price}`)
          .fontColor('#FF6B00')
      }
    }
  }

  // Builder with parameter
  @Builder
  SectionHeader(title: string) {
    Text(title)
      .fontSize(18)
      .fontWeight(FontWeight.Bold)
      .margin({ top: 16, bottom: 8 })
  }

  build() {
    List() {
      ListItem() {
        this.SectionHeader('Featured Products')
      }

      ForEach(this.products, (product: Product) => {
        ListItem() {
          this.ProductItem(product)
        }
      })
    }
  }
}
```

### @BuilderParam (Slots)

```typescript
// Card component with slot
@Component
struct Card {
  @BuilderParam content: () => void = this.defaultContent;
  @BuilderParam footer: () => void = this.defaultFooter;

  @Builder
  defaultContent() {
    Text('Default content')
  }

  @Builder
  defaultFooter() {}

  build() {
    Column() {
      // Content slot
      this.content()

      // Footer slot
      this.footer()
    }
    .padding(16)
    .backgroundColor(Color.White)
    .borderRadius(8)
  }
}

// Usage
@Component
struct ProductPage {
  build() {
    Card() {
      // Content
      Column() {
        Image($r('app.media.product'))
        Text('Product Name')
      }
    }
    .footer(() => {
      Row() {
        Button('Add to Cart')
        Button('Buy Now')
      }
    })
  }
}
```

### @Styles and @Extend

```typescript
// Reusable styles
@Styles
function cardStyle() {
  .backgroundColor(Color.White)
  .borderRadius(12)
  .shadow({ radius: 8, color: '#1A000000' })
  .padding(16)
}

@Styles
function centerStyle() {
  .width('100%')
  .alignItems(HorizontalAlign.Center)
  .justifyContent(FlexAlign.Center)
}

// Extend specific component
@Extend(Text)
function titleStyle() {
  .fontSize(24)
  .fontWeight(FontWeight.Bold)
  .fontColor('#1A1A1A')
}

@Extend(Button)
function primaryButton() {
  .type(ButtonType.Capsule)
  .backgroundColor('#007AFF')
  .fontColor(Color.White)
  .width('100%')
  .height(48)
}

// Usage
@Component
struct StyledPage {
  build() {
    Column() {
      Column() {
        Text('Welcome')
          .titleStyle()
        Text('Description here')
      }
      .cardStyle()

      Button('Get Started')
        .primaryButton()
    }
    .centerStyle()
  }
}
```

## Animations

### Attribute Animation

```typescript
@Component
struct AnimatedButton {
  @State scale: number = 1;
  @State opacity: number = 1;

  build() {
    Button('Animated')
      .scale({ x: this.scale, y: this.scale })
      .opacity(this.opacity)
      .animation({
        duration: 300,
        curve: Curve.EaseInOut
      })
      .onTouch((event: TouchEvent) => {
        if (event.type === TouchType.Down) {
          this.scale = 0.95;
          this.opacity = 0.8;
        } else if (event.type === TouchType.Up) {
          this.scale = 1;
          this.opacity = 1;
        }
      })
  }
}
```

### Explicit Animation

```typescript
@Component
struct ExplicitAnimation {
  @State rotateAngle: number = 0;
  @State translateY: number = 0;

  build() {
    Column() {
      Image($r('app.media.icon'))
        .rotate({ angle: this.rotateAngle })
        .translate({ y: this.translateY })

      Button('Animate')
        .onClick(() => {
          animateTo({
            duration: 1000,
            curve: Curve.EaseInOut,
            iterations: 1,
            playMode: PlayMode.Normal
          }, () => {
            this.rotateAngle = 360;
            this.translateY = 100;
          })
        })
    }
  }
}
```

### Transition Animation

```typescript
@Component
struct TransitionDemo {
  @State isVisible: boolean = false;

  build() {
    Column() {
      Button('Toggle')
        .onClick(() => {
          this.isVisible = !this.isVisible;
        })

      if (this.isVisible) {
        Text('Animated Content')
          .transition({
            type: TransitionType.Insert,
            opacity: 0,
            translate: { y: 50 }
          })
          .transition({
            type: TransitionType.Delete,
            opacity: 0,
            scale: { x: 0.8, y: 0.8 }
          })
      }
    }
  }
}
```

## Gestures

```typescript
@Component
struct GestureDemo {
  @State offsetX: number = 0;
  @State offsetY: number = 0;
  @State scale: number = 1;

  build() {
    Column() {
      Image($r('app.media.photo'))
        .translate({ x: this.offsetX, y: this.offsetY })
        .scale({ x: this.scale, y: this.scale })
        // Pan gesture
        .gesture(
          PanGesture()
            .onActionUpdate((event: GestureEvent) => {
              this.offsetX = event.offsetX;
              this.offsetY = event.offsetY;
            })
        )
        // Pinch gesture
        .gesture(
          PinchGesture({ fingers: 2 })
            .onActionUpdate((event: GestureEvent) => {
              this.scale = event.scale;
            })
        )
        // Combined gestures
        .gesture(
          GestureGroup(GestureMode.Parallel,
            TapGesture({ count: 2 })
              .onAction(() => {
                this.scale = this.scale === 1 ? 2 : 1;
              }),
            LongPressGesture()
              .onAction(() => {
                // Show context menu
              })
          )
        )
    }
  }
}
```

## Dialog and Popup

```typescript
@Component
struct DialogDemo {
  dialogController: CustomDialogController = new CustomDialogController({
    builder: ConfirmDialog({
      title: 'Confirm',
      message: 'Are you sure?',
      onConfirm: () => this.handleConfirm(),
      onCancel: () => this.dialogController.close()
    }),
    autoCancel: true,
    alignment: DialogAlignment.Center
  });

  handleConfirm(): void {
    // Handle confirmation
    this.dialogController.close();
  }

  build() {
    Button('Show Dialog')
      .onClick(() => {
        this.dialogController.open();
      })
  }
}

@CustomDialog
struct ConfirmDialog {
  controller: CustomDialogController = new CustomDialogController({ builder: ConfirmDialog() });
  title: string = '';
  message: string = '';
  onConfirm: () => void = () => {};
  onCancel: () => void = () => {};

  build() {
    Column() {
      Text(this.title)
        .fontSize(18)
        .fontWeight(FontWeight.Bold)

      Text(this.message)
        .margin({ top: 16 })

      Row() {
        Button('Cancel')
          .onClick(() => this.onCancel())
        Button('Confirm')
          .onClick(() => this.onConfirm())
      }
      .margin({ top: 24 })
      .justifyContent(FlexAlign.SpaceEvenly)
      .width('100%')
    }
    .padding(24)
  }
}
```

## Responsive Layout

```typescript
@Component
struct ResponsiveLayout {
  @StorageProp('currentBreakpoint') currentBreakpoint: string = 'sm';

  build() {
    GridRow({
      columns: { sm: 4, md: 8, lg: 12 },
      gutter: { x: 12, y: 12 }
    }) {
      GridCol({ span: { sm: 4, md: 4, lg: 3 } }) {
        this.Sidebar()
      }

      GridCol({ span: { sm: 4, md: 4, lg: 9 } }) {
        this.MainContent()
      }
    }
  }

  @Builder
  Sidebar() {
    Column() {
      // Sidebar content
    }
    .visibility(this.currentBreakpoint === 'sm'
      ? Visibility.None
      : Visibility.Visible)
  }

  @Builder
  MainContent() {
    Column() {
      // Main content
    }
  }
}
```

## Best Practices

### Component Design

```typescript
// ✅ Good: Single responsibility, reusable
@Component
struct Avatar {
  @Prop src: string = '';
  @Prop size: number = 48;
  @Prop borderRadius: number = 24;

  build() {
    Image(this.src)
      .width(this.size)
      .height(this.size)
      .borderRadius(this.borderRadius)
      .objectFit(ImageFit.Cover)
  }
}

// ✅ Good: Composition over inheritance
@Component
struct UserProfile {
  @Prop user: User = new User();

  build() {
    Row() {
      Avatar({ src: this.user.avatar, size: 64 })
      Column() {
        Text(this.user.name)
        Text(this.user.bio)
      }
    }
  }
}
```

### Performance

```typescript
// ✅ Good: Use LazyForEach for large lists
LazyForEach(this.dataSource, (item: Item) => {
  ListItem() {
    ItemCard({ item: item })
  }
}, (item: Item) => item.id)

// ✅ Good: Provide key function for ForEach
ForEach(this.items, (item: Item, index: number) => {
  ItemRow({ item: item })
}, (item: Item) => item.id)  // Key function

// ✅ Good: Avoid unnecessary re-renders
@Component
struct OptimizedList {
  @State @Watch('onDataChange') items: Item[] = [];

  onDataChange(): void {
    // Only called when items actually change
  }
}
```
