# w1nterxt.github.io

个人主页 & 项目展示。

## 结构

```
index.html    — 主页面（单文件，所有样式和脚本内联，方便修改）
README.md     — 本文件
```

## 本地预览

直接用浏览器打开 `index.html`，或者：

```bash
npx serve .
```

## 修改指南

打开 `index.html`，找到 `:root` 下的 CSS 变量即可换主题色：

```css
--accent: #6c63ff;   /* 主色调 */
--bg: #0f0f1a;       /* 背景色 */
```

技能标签在 `#skills` 区块中，项目卡片在 `#projects` 区块中，直接按格式增删就行。
