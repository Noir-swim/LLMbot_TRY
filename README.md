# 🚀 LLMbot_TRY

## 📝 概要
TurtleBot3 を **ROS 2 + Gazebo** 上のシミュレーション環境で動作させ、  
**大規模言語モデル (LLM)** を用いて自然言語の指示からロボットの動作計画を生成・実行するデモです。

---

## 🎯 取り組み内容
- **自然言語 → ロボット動作ステップ計画**  
  LLMを利用して、自然言語の指示を JSON 形式の動作ステップに変換  
  ROS 2 ノードがそれを読み取り、TurtleBot3を制御しました

- **実装した動作例**
  - 指定方向への移動
  - 回転・停止動作
  - 複数ステップの自動生成・連続実行

---

## 📂 実装ファイル
- `gptbot/llm_nav.py` : GPT連携と動作指令ノード  
- `gptbot/llm_nav_thinking.py` : 動作選択ノード  
- `gptbot/llm_task_planner.py` : センサー情報を利用したタスク計画  
- `gptbot/launch/my_house_world.launch.py` : TurtleBot3 環境起動用

---

## 💡 設計
- **OpenAI GPT (LLM)** を使用した動作計画の自動生成  
- **ROS 2 + Gazebo** によるシミュレーション  
- **LiDAR(/scan)・(/odom)**を用いた状態認識  
- GPTの出力：JSON

---
