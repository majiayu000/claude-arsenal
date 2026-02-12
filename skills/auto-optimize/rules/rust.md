# Rust Rules（Rust 特定规则）

Rust 项目扫描和修复的特定规则。从 rnk 项目 30+ session 实战经验提炼。

## 扫描检查项

| ID | 类别 | 检查项 | 严重度 |
|----|------|--------|--------|
| RS-01 | Bug | 嵌套 RwLock/Mutex 获取（死锁风险） | 高 |
| RS-02 | Bug | TOCTOU：get() 后 insert()，中间释放了锁 | 高 |
| RS-03 | Bug | unwrap() 在非测试代码中（panic 风险） | 中 |
| RS-04 | Design | 多个 Signal/Arc 管理同一逻辑状态（应合并为单个） | 中 |
| RS-05 | Design | 同名不同义的类型（如两个 RenderHandle） | 中 |
| RS-06 | Dedup | 相同 match 臂在多个方法中重复 | 中 |
| RS-07 | Dedup | 手动逐字段复制（应用 merge/apply 方法） | 低 |
| RS-08 | Perf | 不必要的 clone()（Copy 类型用 clone、可借用却 clone） | 低 |
| RS-09 | Perf | 热路径中的 format!() 分配（可用 push_str 或预分配） | 低 |

## SKIP 规则（Rust 特定）

| 条件 | 判定 | 理由 |
|------|------|------|
| 用 std::thread 但 cleanup 需要同步 | SKIP | use_effect cleanup 是 FnOnce + Send，不能用 async |
| Signal<T> clone 看起来像"复制" | SKIP | Signal 是 Arc<RwLock>，clone 共享状态，不是复制 |
| 集合 hooks 有相似模式（list/set/map） | SKIP | 各有领域特定方法，宏化是过度设计 |
| derive(Clone) 看起来多余 | 检查 | Signal<T> 要求 T: Clone |
| #[allow(dead_code)] | 检查 | 可能是 WIP 功能，标记为 DEFER 而非删除 |

## 修复模式（经验证有效）

### 多 Signal → 单 Signal
```rust
// Before: 3 个 Signal，嵌套锁风险
struct History<T> {
    past: Signal<Vec<T>>,
    present: Signal<T>,
    future: Signal<Vec<T>>,
}

// After: 单 Signal，原子操作
struct History<T> {
    state: Signal<HistoryState<T>>,
}
struct HistoryState<T> { past: Vec<T>, present: T, future: Vec<T> }
// 所有操作用 state.update(|s| { ... }) 一次完成
```

### TOCTOU → entry API
```rust
// Before: get() 释放锁后 insert()
if !map.get(&key).is_some() { map.insert(key, val); }

// After: 单次 update + entry
signal.update(|m| { m.entry(key).or_insert(val); });
```

### 重复 match → 参数化
```rust
// Before: to_ansi_fg() 和 to_ansi_bg() 各 18 个 match 臂
// After: to_ansi(self, background: bool) 共享一个 match
fn to_ansi(self, background: bool) -> String {
    let base: u8 = if background { 40 } else { 30 };
    match self { Color::Red => format!("\x1b[{}m", base + 1), ... }
}
```

### 重复类型 → 提取共享模块
```rust
// Before: textarea/keymap.rs 和 viewport/keymap.rs 各定义 KeyBinding, KeyType, Modifiers
// After: components/keymap.rs 定义一次，两处 pub use 引入
pub use crate::components::keymap::{KeyBinding, KeyType, Modifiers};
```

## 验证命令
```bash
cargo fmt && cargo clippy && cargo test --lib
```
每个 fix 完成后必须运行。clippy warning 视为失败。
