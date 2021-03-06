o
    ??a?4  ?                   @   s&   d dl Z d dlmZ G dd? d?ZdS )?    N)?Robotc                   @   s?   e Zd Zdd? Zdd? Zdd? Zdd? Zd	d
? Zdd? Zdd? Z	dd? Z
dd? Zdd? Zdd? Zdd? Zdd? Zdd? Zdd? Zdd ? Zd!d"? Zd#d$? Zd%d&? Zd'd(? Zd)d*? Zd+d,? Zd-d.? Zd/d0? Zd1S )2?Basec                 C   s?   || _ || _|| _|| _|| _d| _d| _d| _d| _d| _	|dkr*t
j?d?| _nt
j?d?| _| j?? | _|| j_|| j_d S )Ni?  r   ? ?redzredbase.pngzbluebase.png)?screen?type?_Base__robot_map?_Base__robot_list?_Base__myGame?_Base__SelfElixir?_Base__TotalTeamElixir?_Base__TotalVirus?_Base__MovingAverage?_Base__Signal?pygame?image?load?get_rect?rect?x?y)?selfr   r   r   r   r	   r   ?game? r   ?)C:\Users\5490Latitude\CodeWars-v1\base.py?__init__   s    zBase.__init__c                 C   sj  | j }|d dk s|d |jd krd S |d dk s#|d |jd kr%d S | j|d  |d  dkrC|j|d  |d   |8  < d S | j|d  |d  dkr^| |jkr^|  j|7  _d S | j|d  |d  dkry| |jkry|j?||? d S | j|d  |d  dkr?| |jkr?|  j|7  _d S | j|d  |d  dkr?| |jkr?|j?||? d S | j|d  |d  dkr?| |jkr?|j j|8  _|j j	|8  _	d S | j|d  |d  dkr?| |jkr?|  j|7  _d S | j|d  |d  dk?r| |jk?r|j j|8  _|j j	|8  _	d S | j|d  |d  dk?r1| |jk?r3|  j|7  _d S d S d S )Nr   ?   ?   ?   ?   )
r
   ?
_Game__dimr   ?_Game__resources?_Game__redbaser   ?_Game__bluebase?VirusOnRobotr   r   )r   ?v?pos?gr   r   r   ?actVirus   sF   $$$$$$((?zBase.actVirusc                 C   s    g }| j D ]}|?|j? q|S ?N)r	   ?appendZ_Robot__Signal)r   ?resr   r   r   r   ?GetListOfSignals>   s   
zBase.GetListOfSignalsc                 C   s:   |dk r|  j |8  _ d S |  j|7  _|  j|7  _d S ?Nr   )r   r   r   ?r   r%   r   r   r   ?addResourceD   s   zBase.addResourcec                 C   s?   | j j| }t|?dkr| j j|d  |d   |8  < d S |t|? }g }|D ]G}|j|kra||j }|  j|j8  _|?|? |??  d| j|d  |d < | j j|d  |d   |7  < q(|  j|8  _| j|8  _q(|D ]	}| j j| |= qrd S )Nr   r   )	r
   ?_Game__PositionToRobot?lenr!   ?_Robot__selfElixirr   r*   ?killr   )r   r&   ZvirusZrobots?delete?robot?e?dr   r   r   r$   K   s&    


"?zBase.VirusOnRobotc                 C   sB  | j dkr?d}t|?t|?kst|?dkrd}|  j d8  _ t| j| jj| jj| j|| ?}| j?	|? | jjd | jjd f| j
jv rVd| j
j| jjd | jjd f |< n"i | j
j| jjd | jjd f< d| j
j| jjd | jjd f |< | jdkr?d| j| jjd  | jjd < d S d| j| jjd  | jjd < d S d S )	N?2   ?wncc?   r   Tr   r   r   )r   r   r1   r   r   r   r   r   r	   ?addr
   r0   r   )r   ?signal?str?robor   r   r   ?create_robot_   s   
 & $
""?zBase.create_robotc                 C   s?   | j jdkrdS | j| j jd d  | j jd  dkr$| jdkr"dS dS | j| j jd d  | j jd  dkr@| jdkr>d	S d
S | j| j jd d  | j jd  dkr\| jdkrZdS dS | j| j jd d  | j jd  dkrx| jdkrvd
S d	S dS ?Nr   ?wallr:   r   r   ?friend?enemyr   ?friend-base?
enemy-baser   r   ?blank?r   r   r   r   r   ?r   r   r   r   ?investigate_upr   ?&   &
&
&
&
zBase.investigate_upc                 C   s?   | j jdkrdS | j| j jd d  | j jd  dkr$| jdkr"dS dS | j| j jd d  | j jd  dkr@| jdkr>d	S d
S | j| j jd d  | j jd  dkr\| jdkrZdS dS | j| j jd d  | j jd  dkrx| jdkrvd
S d	S dS ?N?  rA   r:   r   r   rB   rC   r   rD   rE   r   r   rF   rG   rH   r   r   r   ?investigate_down?   rJ   zBase.investigate_downc                 C   s?   | j jdkrdS | j| j jd  | j jd d  dkr$| jdkr"dS dS | j| j jd  | j jd d  dkr@| jdkr>d	S d
S | j| j jd  | j jd d  dkr\| jdkrZdS dS | j| j jd  | j jd d  dkrx| jdkrvd
S d	S dS r@   ?r   r   r   r   r   rH   r   r   r   ?investigate_left?   rJ   zBase.investigate_leftc                 C   s?   | j jdkrdS | j| j jd  | j jd d  dkr$| jdkr"dS dS | j| j jd  | j jd d  dkr@| jdkr>d	S d
S | j| j jd  | j jd d  dkr\| jdkrZdS dS | j| j jd  | j jd d  dkrx| jdkrvd
S d	S dS rK   rN   rH   r   r   r   ?investigate_right?   rJ   zBase.investigate_rightc                 C   s  | j jdks| j jdkrdS | j| j jd d  | j jd d  dkr,| jdkr*dS dS | j| j jd d  | j jd d  d	krJ| jdkrHd
S dS | j| j jd d  | j jd d  dkrh| jdkrfdS dS | j| j jd d  | j jd d  dkr?| jdkr?dS d
S dS )NrL   r   rA   r:   r   r   rB   rC   r   rD   rE   r   r   rF   ?r   r   r   r   r   rH   r   r   r   ?investigate_ne?   ?&   *
*
*
*
zBase.investigate_nec                 C   s  | j jdks| j jdkrdS | j| j jd d  | j jd d  dkr,| jdkr*dS dS | j| j jd d  | j jd d  dkrJ| jdkrHd	S d
S | j| j jd d  | j jd d  dkrh| jdkrfdS dS | j| j jd d  | j jd d  dkr?| jdkr?d
S d	S dS r@   rQ   rH   r   r   r   ?investigate_nw?   rS   zBase.investigate_nwc                 C   s  | j jdks| j jdkrdS | j| j jd d  | j jd d  dkr,| jdkr*dS dS | j| j jd d  | j jd d  dkrJ| jdkrHd	S d
S | j| j jd d  | j jd d  dkrh| jdkrfdS dS | j| j jd d  | j jd d  dkr?| jdkr?d
S d	S dS rK   rQ   rH   r   r   r   ?investigate_se  rS   zBase.investigate_sec                 C   s  | j jdks| j jdkrdS | j| j jd d  | j jd d  dkr,| jdkr*dS dS | j| j jd d  | j jd d  d	krJ| jdkrHd
S dS | j| j jd d  | j jd d  dkrh| jdkrfdS dS | j| j jd d  | j jd d  dkr?| jdkr?dS d
S dS )Nr   rL   rA   r:   r   r   rB   rC   r   rD   rE   r   r   rF   rQ   rH   r   r   r   ?investigate_sw+  rS   zBase.investigate_swc                 C   ?   | j S r)   )r   rH   r   r   r   ?GetYourSignalG  ?   zBase.GetYourSignalc                 C   s.   d}t |?t |?kst|?dkrd S || _d S )Nr9   r:   )r   r1   r   )r   ?sr=   r   r   r   ?SetYourSignalJ  s   
zBase.SetYourSignalc                 C   rW   r)   )r   rH   r   r   r   ?GetTotalElixirO  rY   zBase.GetTotalElixirc                 C   rW   r)   )r   rH   r   r   r   ?	GetElixirQ  rY   zBase.GetElixirc                 C   rW   r)   )r   rH   r   r   r   ?GetVirusS  rY   zBase.GetVirusc                 C   s   | j jd | j jd fS )Nr:   )r   r   r   rH   r   r   r   ?GetPositionV  s   zBase.GetPositionc                 C   ?   | j jd S r-   ?r
   Z	_Game_dimrH   r   r   r   ?GetDimensionXY  ?   zBase.GetDimensionXc                 C   r`   )Nr   ra   rH   r   r   r   ?GetDimensionY\  rc   zBase.GetDimensionYc                 C   s8  || j ks	|dkrd S |  j |8  _ | ?|d | jjd | jjf? | ?|d | jjd | jjf? | ?|d | jjd | jjd f? | ?|d | jjd | jjd f? | ?|d | jjd | jjd f? | ?|d | jjd | jjd f? | ?|d | jj| jjd f? | ?|d | jj| jjd f? d S )Nr   ?   r   )r   r(   r   r   r   r.   r   r   r   ?DeployVirus_  s     $$$$ $zBase.DeployVirusc                 C   s   | j ?| j| j? d S r)   )r   ?blitr   r   rH   r   r   r   ?blitmel  s   zBase.blitmeN)?__name__?
__module__?__qualname__r   r(   r,   r/   r$   r?   rI   rM   rO   rP   rR   rT   rU   rV   rX   r[   r\   r]   r^   r_   rb   rd   rf   rh   r   r   r   r   r      s2    $r   )r   r5   r   r   r   r   r   r   ?<module>   s    