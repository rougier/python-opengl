import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,1.25))
ax = plt.axes([0,0,1,1], frameon=False)

ax.plot([0, 1.00], [.6,.6], color="#bbbbbb", linewidth = 14, solid_capstyle='round')
ax.plot([0, 1.00], [.6,.6], color="#eeeeee", linewidth = 12, solid_capstyle='round')
ax.plot([0, 0.001], [.6,.6], color="#df3651", linewidth = 12, solid_capstyle='round')

plt.xlim(-0.025,1.025)
plt.ylim(0.0,1.0)
plt.xticks([]), plt.yticks([])

big, small = 16, 10
space = .2
color1 = "#000000"
color2 = "#555555"

plt.text(-0.02, 0.85, "Campaign progress",
         va="bottom", weight="bold", fontsize=12, color=color1)

y = 0.22
plt.text(0*space, y, "0%", va="bottom", fontsize=big, color=color1)
plt.text(0*space, y, "funded", va="top", fontsize=small, color=color2)
plt.text(1*space, y, "0€",  va="bottom", fontsize=big, color=color1)
plt.text(1*space, y, "received", va="top", fontsize=small, color=color2)
plt.text(2*space, y, "0",  va="bottom", fontsize=big, color=color1)
plt.text(2*space, y, "backers", va="top", fontsize=small, color=color2)
plt.text(3*space, y, "365",  va="bottom", fontsize=big, color=color1)
plt.text(3*space, y, "days to go", va="top", fontsize=small, color=color2)
plt.text(4*space, y, "May 5, 2018",  va="bottom", fontsize=big, color=color1)
plt.text(4*space, y, "Last update", va="top", fontsize=small, color=color2)

plt.tight_layout()
plt.savefig("crowdfunding.png", dpi=300)
plt.show()
