dims = {
	"Corvette C6": {
		"car_length": 4.47, 
		"car_width": 1.92, 
		"car_height": 1.25, 
		
		"apply_wheels": True, 
		"wheelbase": 2.7, 
		"front_wheel": 0.93, 
		"wheel_radius": 0.33, 
		"wheel_width": 0.22, 
		"wheels_enter_percent": 25., 
		
		"grille_height": 0.64, 
		"hood_angle": 2.5, 
		"hood_length": 1.56, 
		"windshield_angle": 34., 
		"roof_length": 0.88, 
		"roof_angle": -1.3, 
		"rear_window_angle": -14.6, 
		"rear_window_height": 0.22, 
		"trunk_angle": -4., 
		
		"apply_curves": True, 
		"grille_curve": "- 0.008 * (4.75*y)**2 - np.log(1 + np.exp(3*(z-1)))  - 0.03 * (1.15*y)**10 - (0.1 if (z<-0.3 and z>-0.6) else 0.)", 
		"hood_curve": "- 0.01 * (0.65*x + 0.65)**2 - 0.003 * (4.75*y)**2", 
		"roof_curve": "- 0.01 * (1.17*x)**2 - 0.0015 * (4.75*y)**2", 
		"trunk_curve": "- 0.01 * (1.05*(x))**2 - 0.0015 * (4.75*y)**2", 
		"rear_curve": "0.01 * (3.25*y)**2",
		"side_curve": "0.005*(3.25*x)**2 + 0.002*(5*(z+0.5))**2 + 0.02*(1.25*x+0.05)**10 + (0.05+0.2*z if 1.2*z+0.32*x-0.15>0 else -0.05-0.05*(1.25*z+0.32*x-0.15) + 0.05*(1.25*z+0.32*x+0.93)**10)",
        "under_curve": "0.0002*(x-0.8)**12",
	},
    "Ford Mustang 1969": {
		"car_length": 4.76, 
		"car_width": 1.82, 
		"car_height": 1.30, 
		
		"apply_wheels": True, 
		"wheelbase": 2.86, 
		"front_wheel": 0.90, 
		"wheel_radius": 0.33, 
		"wheel_width": 0.22, 
		"wheels_enter_percent": 35., 
		
		"grille_height": 0.64, 
		"hood_angle": 2.5, 
		"hood_length": 1.70, 
		"windshield_angle": 48., 
		"roof_length": 1.06, 
		"roof_angle": -2.55, 
		"rear_window_angle": -14.5, 
		"rear_window_height": 0.22, 
		"trunk_angle": -14.5, 
		
		"apply_curves": True, 
		"grille_curve": "- 0.008 * (4.75*y)**2 - 0.03 * (1.05*y)**10 - (0.1 if (z<0.8 and z>-0.05) else -0.15*(z+0.3) if z<-0.3 else 0.)", 
		"hood_curve": "- 0.001 * (0.65*x + 0.65)**2 - 0.003 * (4.75*y)**2  - 0.05*np.log(1 + np.exp(5*(x-0.5)))", 
		"roof_curve": "- 0.01 * (1.17*x)**2 - 0.0015 * (4.75*y)**2", 
		"trunk_curve": "- 0.01 * (1.05*(x))**2 - 0.0015 * (4.75*y)**2", 
		"rear_curve": "-0.1*(z+0.2) if z<-0.2 else 0.055*(z+0.2)",
		"side_curve": "0.005*(3.25*x)**2 + 0.002*(5*(z+0.5))**2 + 0.02*(1.25*x+0.05)**10 + (0.15*z if 1.2*z-0.13>0 else -0.05-0.05*(1.25*z-0.13) + 0.025*(1.25*z+0.95)**10)",
        "under_curve": "(0.2*(x - 0.5) if x>0.5 else 0.) + (-0.3*(x +0.5) if x<-0.5 else 0)",
    },
    "Ferarri F430": {
		"car_length": 4.51, 
		"car_width": 1.92, 
		"car_height": 1.21, 
		
		"apply_wheels": True, 
		"wheelbase": 2.56, 
		"front_wheel": 1.11, 
		"wheel_radius": 0.33, 
		"wheel_width": 0.22, 
		"wheels_enter_percent": 20., 
		
		"grille_height": 0.63, 
		"hood_angle": 2.5, 
		"hood_length": 1.26, 
		"windshield_angle": 32., 
		"roof_length": 0.73, 
		"roof_angle": 0., 
		"rear_window_angle": -12., 
		"rear_window_height": 0.27, 
		"trunk_angle": 0.9, 
		
		"apply_curves": True, 
		"grille_curve": "- 0.015 * (4.75*y)**2 - 0.005 * (1.12*y)**10 + 0.03*(z-1) + (-0.1 if (1.1*(z+0.2)**2 + 2.5*(abs(y)-0.6)**2 < 0.25) else 0.)  + (-0.1 if (abs(z+0.5)<0.3 and abs(y)<0.2) else 0.)", 
		"hood_curve": "- 0.045*np.log(1 + np.exp(5*(x))) + (-0.03*np.log(1 + np.exp(-10*(abs(y)-0.9))) if abs(y)>0.6 else -0.09) * 1/(1+np.exp(-3*x))", 
		"roof_curve": "- 0.01 * (1.17*x)**2 - 0.0015 * (4.75*y)**2", 
		"trunk_curve": "0", 
		"rear_curve": "(-0.5*(z+0.5) if z<-0.8 else -0.1*(z-0.35) if z<0.25 else -0.4*((z-0.65)**2-0.15)) + 0.005 * (4.75*y)**2 + 0.0002 * (5*y)**4  + (0.1 if z<-0.2 and abs(y)+0.2*(z+1)<0.7 else 0.)  + (-0.025 if (z+0.5)**2+(abs(y)-0.82)**2<0.015 else 0.)",
		"side_curve": "0.005*(3.25*x)**2 + 0.002*(5*(z+0.5))**2 + 0.035*(1.25*x+0.07)**10 + (0.38*(z+0.22) if 1.2*z+0.2*x-0.25>0 else -0.05-0.05*(1.25*z+0.2*x-0.25) + 0.025*(1.25*z+0.2*x+0.97)**10)",
        "under_curve": "0.1*(x-0.6) if x>0.6 else 0.04*(-x+0.6)",
    },
}


def get_dimensions():
    return dims