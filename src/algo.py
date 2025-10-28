"""
## Group-3 (22114022_22114050_22114082) - Boda Yashwanth, Majji Harsha Vardhan and Sadineni Chaitanya
## Date: Oct 28, 2025
## algo.py - Implementation of Voronoi Diagram using Divide and Conquer algorithm
##           Includes divide phase, base cases (2-3 points), merge phase, and convex hull operations
"""

from line import *
from drawline import *
import copy

history_lines = []
history_cvhlines = []

def sol(points : list, pointNum: int, canvas, Lpart = None):
    if pointNum > 3:
        pointsL, pointsR = divide(points, pointNum)
        linesL, cvhL, _, _ = sol(pointsL, len(pointsL), canvas, Lpart=True)
        linesR, cvhR, _, _ = sol(pointsR, len(pointsR), canvas, Lpart=False)
        print("LR: ",pointsL, pointsR)
        # draw_lines(linesL+linesR,canvas)
        # return linesL+linesR
        return *merge(cvhL, cvhR, linesL, linesR, canvas), history_lines, history_cvhlines
    elif pointNum == 3:
        return *solThree(ThreePoints(points[0], points[1], points[2], Lpart=Lpart)), history_lines, history_cvhlines
    elif pointNum == 2:
        return *solTwo(Line(points[0], points[1], Lpart=Lpart)), history_lines, history_cvhlines
    elif pointNum == 1:
        # Single point - return empty lines and the point as convex hull
        return [], [points[0]], history_lines, history_cvhlines
    else:
        # No points - return empty
        return [], [], history_lines, history_cvhlines

def solTwo(line : Line):
    history_lines.append([copy.deepcopy(line)])
    return [line], line.points

def solThree(threePoints : ThreePoints):
    convexHull = threePointConvexhull(threePoints.points)
    res = solveCircumcenter(threePoints)
    if threePoints.isThreeParallel:
        res = res + solveThreeParallel(threePoints, convexHull)
    history_lines.append(copy.deepcopy(res))
    return res, convexHull
    
def divide(points : list, pointNum: int):
    avg_x=0
    for p in points:
        avg_x+=(p[0]/pointNum)
    print("Center x:", avg_x)
    points.sort(key=lambda p: (p[0], p[1]))
    if len(points[:pointNum//2])==len(points[pointNum//2:]):
        return points[:pointNum//2], points[pointNum//2:]
    
    for i in range(pointNum):
        if points[i][0] > avg_x or (i>0 and points[i][0]==points[i-1][0]):
            return points[:i], points[i:]
        
    return points[:pointNum//2], points[pointNum//2:]
 

def merge(cvhL : list, cvhR : list, linesL, linesR, canvas):
    hyperplane_result = []
    history_hyperplane = []
    history_intersection = []
    history_linesIdx = []

    lines = linesL+linesR

    cvhL_lines, cvhR_lines = [Line(cvhL[i], cvhL[nextIndex(i,cvhL)], isConvexHull=True) for i in range(len(cvhL))], [Line(cvhR[i], cvhR[nextIndex(i,cvhR)], isConvexHull=True) for i in range(len(cvhR))]
    history_lines.append([])  # pause for one step
    history_cvhlines.append(copy.deepcopy(cvhL_lines))

    history_lines.append([]) # pause for one step
    history_cvhlines.append(copy.deepcopy(cvhR_lines))

    cvh_lines, cvh, lp, rp, llp, lrp = mergeConvexHull(cvhL, cvhR) # upperTengent: [lp,rp], lowerTengent: [llp,lrp]
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!cvh", cvhL)
    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!cvh", cvhR)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!cvh", cvh)
    
    history_lines.append(copy.deepcopy(lines))
    history_cvhlines.append(copy.deepcopy(cvh_lines))

    LowerTengentLine = Line(llp, lrp, isHyper=1)

    print("\nUpper tangent:",lp,rp,"\nLower tangent:",llp,lrp,'\n')
    while 1:
        print("Tangent:",lp,rp)
        hyperplaneline = Line(lp,rp,isHyper=True)
        history_hyperplane.append(hyperplaneline)
        pairs = getIntersections(hyperplaneline, lines, history_intersection) # [((x,y),idx),((x,y),idx), ...]
        if len(pairs)==0 or (lp == llp and rp == lrp) : # If no intersections appear early, fall back to the lower tangent which will not intersect other bisectors
            #FAILED approach 1: choose the endpoint farther from the initial hyperplane
                # side1 = cal_length(history_hyperplane[0].points[0], LowerTengentLine.points[0]) + cal_length(history_hyperplane[0].points[1], LowerTengentLine.points[0])
                # side2 = cal_length(history_hyperplane[0].points[0], LowerTengentLine.points[1]) + cal_length(history_hyperplane[0].points[1], LowerTengentLine.points[1])
                # LowerTengent_target_side = 1 if side1 < side2 else 0
                # reviseLineByKnown2Points(LowerTengentLine,a=history_intersection[-1],b=LowerTengentLine.canvasLine[LowerTengent_target_side])
            #FAILED approach 2: use dot products to find the farther entry point from the hyperplane and set it as LowerTengentLine.canvasLine[1]
                # reviseCanvasLine([LowerTengentLine], 0, history_hyperplane[-2].canvasLine[0], history_intersection[-1], history_hyperplane[-1].canvasLine[1], remain= False)
            reviseLineByKnown2Points(LowerTengentLine,a=history_intersection[-1],b=LowerTengentLine.canvasLine[1])
            hyperplane_result.append(LowerTengentLine)
            history_lines.append(copy.deepcopy(lines)+copy.deepcopy(hyperplane_result))
            break
        pairs.sort(key= lambda pair : pair[0][1]) # sort by y value, top to bottom
        print("Candidate intersections:",pairs)
        intersection, target_line, idx = pairs[0][0], lines[pairs[0][1]], pairs[0][1]
        history_intersection.append(intersection)
        print(intersection,"added to history_intersection")
        print("Highest priority intersection:",intersection,", bisector of", lines[idx].points)

        # avoid duplicate intersection
        history_linesIdx.append(idx)

        # choose next hyperplane endpoints to continue splitting
        isLeft = True if target_line in linesL else False
        if isLeft:
            # print("lp: ", lp)
            # print("points: ", target_line.points)
            # print("XOR: ", target_line.points.index(lp)^1)
            # print(target_line.points)
            lp = target_line.points[target_line.points.index(lp)^1]
        else:
            # print("rp: ", rp)
            # print("points: ", target_line.points)
            # print("XOR: ", target_line.points.index(rp)^1)
            rp = target_line.points[target_line.points.index(rp)^1]
        print("Next tangent:",lp,rp)

        reviseHyperLine(hyperplaneline, history_intersection) # revise hyperplane
        hyperplane_result.append(hyperplaneline)
        history_lines.append(copy.deepcopy(lines)+copy.deepcopy(hyperplane_result)) # add the line to history
        # debug draw line
        # draw_lines(lines+hyperplane_result, canvas) 


    hascutBorder = []
    # clip bisectors
    i = 0 # hyper id
    for idx in history_linesIdx:
        print("Bisector of",lines[idx].points,"\ni =",i)
        print("Hyperplane start:",history_hyperplane[i].canvasLine[0],", next hyperplane end:",history_hyperplane[i+1].canvasLine[1])
        hascutBorder.append(reviseCanvasLine(lines, idx, history_hyperplane[i].canvasLine[0], history_intersection[i],  history_hyperplane[i+1].canvasLine[1], remain= True))
        i+=1
    for p in hascutBorder:
        deepErase(p,lines)
        
    history_lines.append(copy.deepcopy(lines)+copy.deepcopy(hyperplane_result))
    # reset
    all_lines = lines+hyperplane_result
    for line in all_lines:
        line.isHyper = False
        line.afterMerge = True
        line.remain = False
    history_lines.append(copy.deepcopy(all_lines))
    # debug draw line
    # draw_lines(all_lines, canvas) 
    return all_lines, cvh

def mergeConvexHull(cvhL,cvhR):
    upL, upR = findTangent(cvhL, cvhR, isUpper=1)
    lowL, lowR = findTangent(cvhL, cvhR, isUpper=0)
    i_upL, i_upR, i_lowL, i_lowR = cvhL.index(upL),cvhR.index(upR),cvhL.index(lowL),cvhR.index(lowR)
    merged_cvh = []

    print("in mergeConvexHull cvhL", cvhL)
    print("in mergeConvexHull cvhR", cvhR)
    print("mergeConvexHull upper tangent:", upL, upR)
    print("mergeConvexHull lower tangent:", lowL, lowR)

    # walk the left hull counterclockwise from lowL up to and including upL
    i = i_lowL
    merged_cvh.append(cvhL[i])
    while i != i_upL:
        i = nextIndex(i,cvhL)
        # i = len(cvhL)-1 if i-1<0 else i-1
        merged_cvh.append(cvhL[i])

    # walk the right hull counterclockwise from upR down to and including lowR
    i = i_upR
    merged_cvh.append(cvhR[i])
    while i != i_lowR:
        i = nextIndex(i,cvhR)
        # i = len(cvhR)-1 if i-1<0 else i-1
        merged_cvh.append(cvhR[i])

    upT_i, lowT_i = merged_cvh.index(upL), merged_cvh.index(lowR)

    cvh_lines = [Line(merged_cvh[i], merged_cvh[nextIndex(i,merged_cvh)], isConvexHull=True, isTengent= True if i==upT_i or i==lowT_i else False) for i in range(len(merged_cvh))]

    return cvh_lines, merged_cvh, upL, upR, lowL, lowR

def findTangent(pointsL, pointsR, isUpper=1):

    lp,rp = max(pointsL, key=lambda p: (p[0], p[1])), min(pointsR, key=lambda p: (p[0], -p[1]))
    # print("in findtengent: ",lp,rp)

    orderL = pointsL[::-1] if isUpper else pointsL[:] # upper tangent: left CCW, right CW
    orderR = pointsR[:] if isUpper else pointsR[::-1] # lower tangent: left CW, right CCW

    # print("Upper tangent",isUpper, " orderL:", orderL)
    # print("Upper tangent",isUpper, " orderR:", orderR)

    iL,iR = orderL.index(lp), orderR.index(rp)

    while True:
        # if isUpper == 0:
        #     print("debuging 1: ", orderL[iL],orderR[iR]) 
        moved = False
        while isClockwise(orderR[iR], orderL[iL], orderL[nextIndex(iL,orderL)]) == isUpper:
            iL = nextIndex(iL,orderL)
            moved = True
            # if isUpper == 0:
            #     print("debuging 2: ", orderL[iL],orderR[iR]) 
        while isClockwise(orderL[iL], orderR[iR], orderR[nextIndex(iR,orderR)]) == (isUpper ^ 1):
            iR = nextIndex(iR,orderR)
            moved = True
            # if isUpper == 0:
            #     print("debuging 2: ", orderL[iL],orderR[iR]) 
        if not moved:
            break
    return orderL[iL], orderR[iR]

def cal_crossprod(a, b, c): #Vab to Vac
    # vector A => AB = b - a
    # vector B => AC = c - a
    vA = b[0] - a[0], b[1] - a[1]
    vB = c[0] - a[0], c[1] - a[1]
    cross = vA[0]*vB[1]-vB[0]*vA[1]
    # cross product
    # va = (ax, ay), vb = (bx, by)
    # va x vb = | ax ay |
    #           | bx by | = ax*by-bx*ay
    return cross

def isClockwise(a, b, c):
    cross = cal_crossprod(a, b, c) #Vab to Vac
    if cross > 0:
        return 1
    elif cross < 0:
        return 0
    else:
        return -1 # colinear (angle is 0 or 180 degrees)

def nextIndex(idx, li):
    return (idx+1) % len(li)
    
def chooseEndPoint(p1, p2, p3, p4):
    cross1 = cal_crossprod(p1, p2, p3)
    cross2 = cal_crossprod(p1, p2, p4)
    # cross > 0 => counterclockwise, choose the smaller turn
    if cross1 > 0 and cross2 <= 0:
        return p3
    elif cross2 > 0 and cross1 <= 0:
        return p4
    elif cross1 > 0 and cross2 > 0: # both counterclockwise, pick the smaller rotation
        return p3 if cross1 < cross2 else p4
    else:                           # both clockwise or colinear, choose the smaller rotation
        return p3 if abs(cross1) < abs(cross2) else p4

def cal_length(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def threePointConvexhull(li : list):
    cross = cal_crossprod(li[0], li[1], li[2])
    if cross == 0:
        sorted_li = sorted(li, key=lambda p: (p[0], p[1]))
        return [sorted_li[0], sorted_li[-1]]
    if cross > 0:
        return li   # already CCW
    else:
        return li[::-1]

def solveThreeParallel(threePoints : ThreePoints, convexhull) -> list[Line]:
    result = []
    end1, end2 = convexhull
    for line in threePoints.lines:
        if (end1 in line.points) ^ (end2 in line.points):
            result.append(line)
    return result

def solveCircumcenter(threePoints : ThreePoints):
    no_circumcenter = threePoints.isThreeParallel
    print(f'Circumcenter exists: {not no_circumcenter}')
    # print(f'Counterclockwise order:{threePoints.points}')
    if not no_circumcenter:
        circumcenter = threePoints.circumcenter
        print(f'Circumcenter: {circumcenter}')
        return cut(threePoints, circumcenter)
    return []

def cut(threePoints : ThreePoints, circumcenter) -> list[Line]:
    result = []
    vertiVectors = threePoints.vertiVectors
    d = 99999 # extend length
    for i in range(len(vertiVectors)):
        v = vertiVectors[i]
        # extend_point = (x + d * vectorX, y + d * vectorY)
        p = (circumcenter[0] + d * v[0], circumcenter[1] + d * v[1])
        # canvas.create_oval(p1[0] - 3, p1[1] - 3, p1[0] + 3, p1[1] + 3, fill='black')
        # canvas.create_oval(p2[0] - 3, p2[1] - 3, p2[0] + 3, p2[1] + 3, fill='black')
        threePoints.lines[i].canvasLine = [circumcenter, p]
        threePoints.lines[i].canvasLine = threePoints.lines[i].canvasLine[:]
        result.append(threePoints.lines[i])
        # draw_line(canvas, circumcenter, p)
    return result

def has_duplicates(points):
    return True if len(points) != len(set(points)) else False

def getIntersections(line1 : Line, lines: list[Line], history_intersection):
    p1, m1= line1.center, line1.verticalSlope
    pairs = []
    for i, line in enumerate(lines):
        p2, m2 = line.center, line.verticalSlope
        x, y = getIntersection(p1,m1,p2,m2)
        if line.erase: # already removed
            continue
        if len(history_intersection) and (y < history_intersection[-1][1] and not isSameValue(y,history_intersection[-1][1])): # hyperplane intersections should move downward
            print("Above previous intersection",x, y)
            continue
        if len(history_intersection) and isSamePoint((x,y), history_intersection[-1]):
            print("Already processed this intersection; skip to avoid infinite loop",x, y)
            continue
        if (x,y) == (float('inf'),float('inf')):
            print("Parallel, no intersection",x, y)
            continue
        if not on_segment((x,y),line.canvasLine):
            print(f"Not on segment: {(x,y)} not on {line.canvasLine}")
            continue
        pairs.append(((x,y),i)) # tuple(intersection,idx)
    return pairs

def getIntersection(p1, m1, p2, m2):
    if m1 == m2:
        return (float('inf'),float('inf'))  # parallel or coincident, no intersection
    x = (m1 * p1[0] - m2 * p2[0] + p2[1] - p1[1]) / (m1 - m2)
    y = m1 * (x - p1[0]) + p1[1]
    return (x, y)

def isSameValue(v1,v2):
    thres = 0.1
    return 1 if abs(v1-v2)<thres and abs(v1-v2)<thres else 0

def isSamePoint(p1,p2):
    x1,y1,x2,y2 = p1[0],p1[1],p2[0],p2[1]
    return 1 if isSameValue(x1,x2) and isSameValue(y1,y2) else 0

def on_segment(p, seg):
    (x, y) = p
    (x1, y1), (x2, y2) = seg
    thres = 0.01
    # Allowable slight errors
    return (min(x1, x2)-thres <= x <= max(x1, x2)+thres and
            min(y1, y2)-thres <= y <= max(y1, y2)+thres)

def reviseLineByKnown2Points(line, a=None, b=None):
    if a==None and b:
        line.canvasLine[1] = b
    if a and b==None:
        line.canvasLine[0] = a
    if a and b:
        line.canvasLine = [a, b]
    return
    # keep segment order; place new intersection at index 1

def reviseHyperLine(line, history_intersection):
    if len(history_intersection) == 1:
        reviseLineByKnown2Points(line,a=None,b=history_intersection[-1])
    elif len(history_intersection) > 1:
        reviseLineByKnown2Points(line,a=history_intersection[-2],b=history_intersection[-1])
    return

def reviseCanvasLine(lines, i, hyper1point_upper, intersection, hyper2point_lower, remain=True):
    # If the hyperplane turns in the same direction as the boundary edge, remove that side (connect to the opposite boundary)
    cross_hyper = isClockwise(hyper1point_upper, intersection, hyper2point_lower) # v1(upper point to intersection), v2(intersection to lower point)
    cross_upper_border1 = isClockwise(hyper1point_upper,intersection,lines[i].canvasLine[0])
    cross_upper_border2 = isClockwise(hyper1point_upper,intersection,lines[i].canvasLine[1])
    # print("Direction H1->H2:",cross_hyper)
    # print(f"Direction H1->{line.canvasLine[0]}:", cross_upper_border1)
    # print(f"Direction H1->{line.canvasLine[1]}:", cross_upper_border2)
    # cpy = set(line.canvasLine[:])
    # print("Before Cut:", cpy)
    cpy = lines[i].canvasLine[:]
    if cross_hyper == cross_upper_border1:
        lines[i].canvasLine = [intersection, lines[i].canvasLine[1]]
        otherSide = cpy[0]
    elif cross_hyper == cross_upper_border2:
        lines[i].canvasLine = [intersection, lines[i].canvasLine[0]]
        otherSide = cpy[1]

    lines[i].remain = remain
    return otherSide

def deepErase(cutPoint, lines):
    for l in lines:
        if cutPoint in l.canvasLine:
            if l.erase or l.remain:
                continue
            l.erase = True
            # print("next Cut point:", l.canvasLine[l.canvasLine.index(cutPoint)^1])
            deepErase(l.canvasLine[l.canvasLine.index(cutPoint)^1], lines)
    return
