import os
import re
import json
import time
from datetime import datetime
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from dotenv import load_dotenv
from openai import OpenAI

class GPTNav(Node):
    def __init__(self, user_command):
        super().__init__('gpt_nav')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.done = False

        # OpenAI APIキー設定
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

        # ログ保存先
        self.log_dir = os.path.expanduser("~/gptbot_logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # GPTに送るプロンプト（ユーザー指示を埋め込み）
        prompt = f"""
        あなたはロボットの動作計画を出力するアシスタントです。
        ユーザーの指示を、必ず1つのJSONオブジェクトで返してください。
        余分な文章は禁止。出力例:
        {{
          "steps": [
            {{"linear_x": 0.2, "angular_z": 0.0, "duration": 2.0}},
            {{"linear_x": 0.0, "angular_z": 1.0, "duration": 1.0}},
            {{"linear_x": 0.0, "angular_z": 0.0, "duration": 1.0}}
          ]
        }}
        ユーザーの命令: {user_command}
        """
        self.log_and_print("=== GPTに送信したプロンプト ===\n" + prompt)

        # GPT呼び出し
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=300,
            temperature=0
        )

        gpt_reply = response.choices[0].text.strip()
        self.log_and_print("=== GPTの返答 ===\n" + gpt_reply)

        # JSON抽出
        match = re.search(r'\{.*\}', gpt_reply, re.DOTALL)
        if not match:
            self.log_and_print("JSONブロックが見つかりません")
            self.done = True
            return

        json_str = match.group(0)
        try:
            instructions = json.loads(json_str)
            self.execute_steps(instructions["steps"])
        except Exception as e:
            self.log_and_print(f"JSON parse error: {e}")
            self.done = True

    def log_and_print(self, message):
        self.get_logger().info(message)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join(self.log_dir, f"gpt_log_{timestamp}.txt")
        with open(log_path, "a") as f:
            f.write(message + "\n\n")

    def execute_steps(self, steps):
        for i, step in enumerate(steps):
            twist = Twist()
            twist.linear.x = step.get("linear_x", 0.0)
            twist.angular.z = step.get("angular_z", 0.0)
            self.publisher_.publish(twist)
            msg = f"[{i+1}/{len(steps)}] 実行中: {step}"
            self.log_and_print(msg)
            time.sleep(step.get("duration", 1.0))

        # 停止
        self.publisher_.publish(Twist())
        self.log_and_print("全ての動作が終了しました。停止します。")
        self.done = True

def main(args=None):
    # ユーザー入力を受け付ける
    user_command = input("ロボットに何をさせますか？: ")
    rclpy.init(args=args)
    node = GPTNav(user_command)

    while rclpy.ok() and not node.done:
        rclpy.spin_once(node, timeout_sec=0.1)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
