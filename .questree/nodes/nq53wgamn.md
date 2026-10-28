---
id: nq53wgamn
title: 重複セクションの修正とビルド番号の決まり
icon: 🔢
kind: task
stage: candidate
status: done
parent: nxb3i8x8n
edges:
  - { to: ny6ji63zv, type: depends }
files:
  - { path: tools/build.py }
  - { path: tools/check_format.py }
rev: 2
created: 2026-10-28T07:03:37.752Z
updated: 2026-10-28T07:03:37.763Z
---

2.0 用は x.y.0、2.1 用は x.y.1。1ファイル内の重複セクションは Factorio が拒否するので check_format.py で防ぐ。
