import random, time, sys

symbols = ['🍒', '7️⃣', '🍋', '⭐', '🔔', '💎']

def slot_spin_animation(spin_time=2.5, delay=0.05):
    reels = [[], [], []]
    start_time = time.time()

    while time.time() - start_time < spin_time:
        for i in range(3):
            reels[i] = random.choice(symbols)
        sys.stdout.write(
            f"\r🎰 [ {reels[0]} | {reels[1]} | {reels[2]} ]"
        )
        sys.stdout.flush()
        time.sleep(delay)

    print()  
    return reels
