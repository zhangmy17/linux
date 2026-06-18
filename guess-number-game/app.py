from flask import Flask, request, jsonify, session, render_template_string
import random
import os

app = Flask(__name__)
app.secret_key = 'game-secret-key'

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🎯 数字猜猜乐</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; margin: 0; }
        .container { background: white; border-radius: 20px; padding: 30px; max-width: 500px; width: 100%; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
        h1 { text-align: center; }
        button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
        .message { background: #f0f0f0; padding: 15px; border-radius: 10px; margin: 15px 0; }
        .guess-history span { display: inline-block; padding: 5px 12px; margin: 3px; background: #667eea; color: white; border-radius: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 数字猜猜乐</h1>
        <input type="text" id="playerName" placeholder="你的名字" value="Player">
        <button onclick="startGame()">开始游戏</button>
        <div id="gameStatus">请输入名字并开始游戏</div>
        <input type="number" id="guessInput" placeholder="输入数字" min="1" max="100" disabled>
        <button onclick="makeGuess()" id="guessBtn" disabled>猜</button>
        <div id="message" class="message">👋 欢迎！</div>
        <div id="guessHistory"></div>
        <h3>🏆 排行榜</h3>
        <div id="leaderboard"></div>
    </div>
    <script>
        let gameActive = false;
        async function startGame() {
            const playerName = document.getElementById('playerName').value || 'Anonymous';
            const response = await fetch('/api/game/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({player_name: playerName})
            });
            if (response.ok) {
                gameActive = true;
                document.getElementById('gameStatus').textContent = '🎮 游戏进行中 (1-100)';
                document.getElementById('guessInput').disabled = false;
                document.getElementById('guessBtn').disabled = false;
                document.getElementById('message').textContent = '💡 输入你的猜测！';
                document.getElementById('guessHistory').innerHTML = '';
            }
        }
        async function makeGuess() {
            if (!gameActive) return alert('请先开始游戏！');
            const input = document.getElementById('guessInput');
            const number = parseInt(input.value);
            if (isNaN(number) || number < 1 || number > 100) return alert('请输入1-100的数字！');
            const response = await fetch('/api/game/guess', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({number: number})
            });
            const data = await response.json();
            document.getElementById('message').textContent = data.message;
            if (data.guesses) {
                document.getElementById('guessHistory').innerHTML = data.guesses.map(g => `<span>${g}</span>`).join('');
            }
            if (data.is_win) {
                gameActive = false;
                document.getElementById('guessInput').disabled = true;
                document.getElementById('guessBtn').disabled = true;
                document.getElementById('gameStatus').textContent = '🎉 游戏结束！';
                loadLeaderboard();
            }
            input.value = '';
            input.focus();
        }
        async function loadLeaderboard() {
            const response = await fetch('/api/game/leaderboard');
            const data = await response.json();
            const div = document.getElementById('leaderboard');
            if (data.length === 0) { div.innerHTML = '<p style="color:#999;">暂无记录</p>'; return; }
            div.innerHTML = data.map((p, i) => `
                <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #eee;">
                    <span>${i+1}. ${p.username}</span>
                    <span>🏆 ${p.best_score} 次</span>
                </div>
            `).join('');
        }
        document.getElementById('guessInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') makeGuess();
        });
        loadLeaderboard();
    </script>
</body>
</html>
'''


@app.route('/')
def index():
    return HTML


@app.route('/api/game/start', methods=['POST'])
def start_game():
    data = request.get_json()
    player_name = data.get('player_name', 'Anonymous')
    target = random.randint(1, 100)
    session['game'] = {
        'target': target,
        'attempts': 0,
        'guesses': [],
        'player_name': player_name
    }
    return jsonify({'message': '游戏已开始！', 'range': [1, 100]})


@app.route('/api/game/guess', methods=['POST'])
def make_guess():
    if 'game' not in session:
        return jsonify({'error': '请先开始游戏'}), 400

    data = request.get_json()
    guess = data.get('number')
    if not guess:
        return jsonify({'error': '请提供数字'}), 400

    game = session['game']
    target = game['target']
    attempts = game['attempts'] + 1
    guesses = game['guesses']
    guesses.append(guess)

    if guess == target:
        status = 'win'
        message = f'🎉 猜对了！数字是 {target}！用了 {attempts} 次'
    elif guess < target:
        status = 'continue'
        message = '⬆️ 太小了！'
    else:
        status = 'continue'
        message = '⬇️ 太大了！'

    game['attempts'] = attempts
    game['guesses'] = guesses
    session['game'] = game

    if status == 'win':
        session.pop('game', None)

    return jsonify({
        'message': message,
        'attempts': attempts,
        'guesses': guesses,
        'status': status,
        'is_win': status == 'win'
    })


@app.route('/api/game/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify([])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)