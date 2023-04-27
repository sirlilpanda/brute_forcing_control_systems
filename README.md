# brute_forcing_control_systems

## how to use it

- to start brute forcing your system, 
- input your control system into G_CL on line 36,
    ```py
    G_CL = scipy.signal.lti([beta*kp, beta*ki], [1, alpha+beta*kd, delta+beta*kp, beta*ki])
    ```
- next set the ranges you want to search your gains, why the resultion you want to search through them
```py
# (start_value, end_value, resultion)
kp_settings = (0.7, 1.5, 0.001)
ki_settings = (0, 0.3, 0.01)
kd_settings = (0.2, 0.4, 0.001)
```
- set youre input to the control system
```py
# (start_value, end_value, resultion)
sim_settings = (0, 50, 0.01)

#basline value
r0 = 0

#step amount
r_s = np.pi/2

#set after 1
r  = np.array([r0 if x < 1 else r_s for x in t])

```

- finally to run use, this just allows you to easily collect all gains in one file
```sh
python bruteforce.py >> out.csv
```
