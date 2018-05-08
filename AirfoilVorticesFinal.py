from numpy import sin,cos,array
from visual import sphere,color,rate,display,arrow

def f(val,t): #vorticity vector
    r = val[0]
    th = val[1]
    z = val[2]
    dr = 3*dP*t
    dth = 0.01
    dz = v_inlet*0.01
    return array([dr,dth,dz],dtype=float)

def rk4(val,t):
    k1 = f(val,t)
    k2 = f(val+0.5*k1,t+0.5*h)
    k3 = f(val+0.5*k2,t+0.5*h)
    k4 = f(val+k3,t+h)
    dval = (k1+2*k2+2*k3+k4)/6
    val += dval
    return array([val,dval],dtype=float)
    
#define constants and lists
r = []
th = []
z = []
vr = []
vth = []
vz = []
t = []
velvec = {}

#
h = 1e-5
i = 0
iterations = 5000

v_inlet = float(input('Enter a freestream velocity (mph):')) #165 #freestream (mph) typical for airliner takeoff
dP = float(input('Enter a pressure difference:'))#3 #pressure difference induced by wing (atm/atm)

#initialize and set values
t.append(0.0)
vr.append(0.0)
vth.append(0.01)
vz.append(v_inlet)
val = array([0.1,0.0,0.0],dtype=float)
dval = array([0.0,0.0,0.0],dtype=float)
out = ([val,dval])

#solve for vortex ryz coordinates over time
while(i < iterations):
    r.append(val[0])
    th.append(val[1])
    z.append(val[2])
    vr.append(dval[0])
    vth.append(dval[1])
    vz.append(dval[2])
    out = rk4(val,t[i])
    val = out[0]
    dval = out[1]
    t.append(t[i]+h)
    i += 1

#display vortex
scene = display(title='Airfoil Induced Vortex',width=1280, height=1024, center=[0,0,0], background=color.black)
scene.cursor.visible = False
views = [[1,0,0],[1,-1,-1],[0,0,-1]] #side, iso, z
scene.forward = views[1]
vortex = sphere(pos=[0,0,0],radius=0.01,make_trail=True)
vortex.color = color.blue
vl = sphere(pos=[0,0,0],radius=0.01,make_trail=True)
vl.trail_object.color = (0,0.8,0)

#scale rate of animation and size of vectors
scaleAnim = 500
scaleVec = 0.05

#display the position, vortex line, and velocity vectors of the vortex
for i in range(0,iterations):
    rate(scaleAnim)
    vortex.pos = [r[i]*cos(th[i]),r[i]*sin(th[i]),z[i]]
    vl.pos = [0,0,z[i]]
    pos1 = array([r[i]*cos(th[i]),r[i]*sin(th[i]),z[i]])
    
    #adjust view - ONLY for isometric view (view[1])
    if(i < (iterations*3/4)):
        scene.center = [0,0,z[i]]
        
    #show velocity vector every 75 iterations
    if(i%75 == 0):        
        prev = array([r[i-1]*cos(th[i-1]),r[i-1]*sin(th[i-1]),z[i-1]])
        vel = (pos1-prev)/(t[i]-t[i-1])
        j = i/50
        velvec[j] = arrow(pos=pos1, axis=vel*scaleVec*t[i], shaftwidth=5*scaleVec)
        velvec[j].color = (0,0.75,1)
        
#calculate initial freestream velocity and pressure difference based on final iteration
dPcalc = (r[iterations-1]-r[iterations-2])/(t[iterations-1]-t[iterations-2])/t[iterations-1]/3*h
print('Initial Freestream Velocity:',(z[iterations-1]-z[iterations-2])*100,'mph')
print('Initial Pressure Difference:',dPcalc)
