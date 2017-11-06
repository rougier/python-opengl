import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


N4 = np.linspace(0,1,9, endpoint=True)[1:-1:2]
G4 = np.dstack(np.meshgrid(N4,N4)).reshape(len(N4)**2,2)
N8 = np.linspace(0,1,17, endpoint=True)[1:-1:2]
G8 = np.dstack(np.meshgrid(N8,N8)).reshape(len(N8)**2,2)
offsets = { "1 sample"   : [(0.5,0.5)],
            "1x2 sample" : [(0.50, 0.25), (0.50, 0.75)],
            "2x1 sample" : [(0.25, 0.50), (0.75, 0.50)],
            "quincux"    : [(.05,.05), (.95,.05), (.05,.95), (.95,.95), (0.5,0.5)],
            "2x2 grid"   : [(0.25,0.25), (0.75,0.25), (0.25,0.75), (0.75,0.75)],
            "2x2 RGSS"   : G4[[2,4,11,13]],
            "4x4 checker": G4[[0,2,5,7,8,10,13,15]],
            "8 rooks"    : G8[[4,10,16,30,33,47,53,59]],
            "4x4 grid"   : G4,
            "8x8 checker": G8[[ 0, 2, 4, 6, 9,11,13,15,16,18,20,22,25,27,29,31,
                               32,34,36,38,41,43,45,47,48,50,52,54,57,59,61,63]],
            "8x8 grid"   : G8,
            "SDF"        : [(0.5,0.5)] }

# T = np.linspace(0,1,len(N4)+1, endpoint=True)
# T = np.linspace(0,1,len(N8)+1, endpoint=True)

fig, axes = plt.subplots(figsize=(10,4.5), nrows=4, ncols=9)

for i, name in enumerate(offsets.keys()):

    row = i%4
    col = 3*(i//4)
    
    ax = axes[row,col]
    ax.set_aspect(1)
    # ax.set_title(name)

    if name != "SDF":
        P = np.array(offsets[name])
        s = 25 + 25*(1-len(P)/64)
        ax.scatter(P[:,0],P[:,1], s=s, edgecolor="k", facecolor="w")
    else:
        ax.text(.5,.5,"SDF", ha="center", va="center", fontsize=16, fontweight="bold")
        # ax.set_facecolor("0.90")
        ax.set_axis_off()
            
    ax.set_xlim(0,1)
    ax.set_ylim(1,0)
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])

    ax = axes[row,col+1]
    ax.set_axis_off()
    if name != "SDF":
        filename = "triangle-ssaa-filled-%s.png" % name
    else:
        filename = "triangle-sdf-filled.png"
    img = mpimg.imread(filename)
    ax.imshow(img, interpolation="nearest")
    ax.set_xticks([]), ax.set_yticks([])
    
    ax = axes[row,col+2]
    ax.set_axis_off()
    if name != "SDF":
        filename = "triangle-ssaa-outlined-%s.png" % name
    else:
        filename = "triangle-sdf-outlined.png"
    img = mpimg.imread(filename)
    ax.imshow(img, interpolation="nearest")
    ax.set_xticks([]), ax.set_yticks([])
    
plt.tight_layout(pad=0.5, w_pad=0.1, h_pad=.1)
plt.savefig("ssaa-sdf.png", dpi=300)
plt.show()
