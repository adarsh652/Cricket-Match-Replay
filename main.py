import pandas as pd
import matplotlib.pyplot as plt

# Load mock match data
df = pd.read_csv(r"C:\Users\iadar\OneDrive\Desktop\cricket_match_replay\data\mockData.csv")

total_runs = 0
wickets = 0

runs_per_over = {}

print("🏏 Match Replay Started\n")

for index, row in df.iterrows():
    over = row["over"]
    ball = row["ball"]
    batsman = row["batsman"]
    bowler = row["bowler"]
    runs = row["runs"]
    is_wicket = row["is_wicket"]

    # Update match state
    total_runs += runs
    if is_wicket == 1:
        wickets += 1

    # Update runs per over
    if over not in runs_per_over:
        runs_per_over[over] = 0
    runs_per_over[over] += runs

    # Commentary
    event = "WICKET!" if is_wicket == 1 else f"{runs} run(s)"
    print(
        f"{over}.{ball} → {batsman} vs {bowler} : {event} | "
        f"Score: {total_runs}/{wickets}"
    )

print("\n🏁 Match Replay Finished")

# ---------- ANALYTICS ----------

overs = list(runs_per_over.keys())
runs = list(runs_per_over.values())

run_rate = total_runs / len(overs)

print("\n📊 Match Analytics")
print("Runs per over:", runs_per_over)
print("Run Rate:", round(run_rate, 2))

# ---------- MOMENTUM GRAPH ----------

plt.plot(overs, runs)
plt.xlabel("Over")
plt.ylabel("Runs")
plt.title("Momentum Graph (Runs per Over)")
plt.show()


import math

# ---------- WAGON WHEEL ----------

angles = []
distances = []
colors = []

for index, row in df.iterrows():
    runs = row["runs"]

    if runs == 0:
        continue  # skip dot balls

    # Simulated angle (in radians)
    angle = index * 20 % 360
    angle = math.radians(angle)

    # Distance based on runs
    distance = runs * 10

    angles.append(angle)
    distances.append(distance)

    # Color coding
    if runs == 4:
        colors.append("green")
    elif runs == 6:
        colors.append("red")
    else:
        colors.append("blue")

# Convert polar to cartesian
x = [d * math.cos(a) for d, a in zip(distances, angles)]
y = [d * math.sin(a) for d, a in zip(distances, angles)]

# Plot wagon wheel
plt.figure()
plt.scatter(x, y, c=colors)
plt.axhline(0)
plt.axvline(0)
plt.title("Wagon Wheel")
plt.xlabel("Off Side")
plt.ylabel("Leg Side")
plt.show()

import random

# ---------- PITCH MAP ----------

pitch_x = []
pitch_y = []

for _ in range(len(df)):
    # Simulated pitch locations
    x = random.uniform(-1, 1)   # line
    y = random.uniform(0, 20)   # length

    pitch_x.append(x)
    pitch_y.append(y)

plt.figure()
plt.scatter(pitch_x, pitch_y)
plt.gca().invert_yaxis()
plt.title("Pitch Map (Bowling Length & Line)")
plt.xlabel("Line (Off ↔ Leg)")
plt.ylabel("Length (Short → Full)")
plt.show()


# ---------- REPLAY CONTROLLER ----------

current_ball = 0

print("\n🎮 Manual Replay Mode")
print("Press ENTER to see next ball, or type 'q' to quit\n")

while current_ball < len(df):
    user_input = input()

    if user_input.lower() == "q":
        print("Replay stopped.")
        break

    row = df.iloc[current_ball]

    over = row["over"]
    ball = row["ball"]
    batsman = row["batsman"]
    bowler = row["bowler"]
    runs = row["runs"]
    is_wicket = row["is_wicket"]

    event = "WICKET!" if is_wicket == 1 else f"{runs} run(s)"

    print(
        f"{over}.{ball} → {batsman} vs {bowler} : {event}"
    )

    current_ball += 1
