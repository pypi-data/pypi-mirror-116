/*
C-library for Univariate B-splines implementation (nonperiodic & nonuniform).
All function parameters must be passed by address.

This module includes the following functions:
- Driver functions (solves a complete problem):
    CurvePoint
    CurveEval
    CurveDerivsAlg1
    CurveDerivsEval
    CurveDerivCptsAlg1
    CurveDerivCptsAlg2
    CurveAntiDerivCpts
    CurveKnotIns
    RemoveCurveKnot
    RemoveCurveKnots
    RemoveCurveKnotWithoutTol
    DegreeElevateCurve
    SolveTridiagonal
    RefineKnotVectCurve
    CurvesProduct
    Bernstein
    PointOnBezierCurve
    BezierCurveEval
    deCasteljau1
    BezierCurveEval2

- Computational functions (performs a distinct computational task):
    FindSpan
    FindSpanMult
    BasisFuns
    OneBasisFun
    EquallySpaced
    AveragingAlg1
    AveragingAlg2
    AveragingAlg3
    KnotsEvalL2Approx
    DersBasisFuns
    IncreaseMultByOne
    GetBezierMatrix
    BezierProduct
    AllBernstein
    GetRemovalBndCurve

- Auxiliary functions:
    IsClose
    Bin
    ValidKnotVector
    ProductMatrix
    GetBezierMatrixElement


All Driver functions have a diagnostic argument 'info' that indicates the
success or failure of the computation, as follows: 

info = 0 : successful termination
info < 0 : if info = -i, the i-th argument had an illegal value
info > 0 : the algorithm failed. See following table:

info value      Error
----------      ----------------------------
1               memory error
2               division zero error
3               not implemented
4               maximum number of iterations
5               out of range
6               generic failure

References
----------
[1] Carl de Boor, A Pratical Guide to Splines, New York: Springer-Verlag, 2001.
[2] Piegl, L. A., & Tiller, W. (1997). The NURBS book. Berlin: Springer.
[3] Larry L. Schumaker, Spline Functions: Basic Theory, Chapter 5
[4] Tiller, W., Knot-removal algorithms for NURBS curves and surfaces, CAD,
    Vol. 24, No. 8, pp. 445-453, 1992.
[5] Algorithm for computing the product of two B-splines, in A. Le Mehaute,
    C. Rabut, and L. L. Schumaker (eds.) Curves and surfaces with applications
    in CAGD, Vanderbilt University Press, Nashville, TN, 1997, pp 337-344.
[6] Elber, G., Free form surface analysis using a hybrid of symbolic and
    numeric computation, PhD Thesis, Univesrity of Utah, 1992
[7] Piegl, L. & Tiller, W.. (2000). Curve Interpolation with Arbitrary
    End Derivatives. Engineering with Computers. 16. 73-79.
    
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "ubsplclib.h"

int Bin(int n, int k)
{
    /* Computes the binomial coefficient */
    int i, j;
    int C[k + 1];
    
    memset(C, 0, sizeof(C));
    C[0] = 1;
    
    for (i = 1; i <= n; ++i)
        for (j = MIN(i, k); j > 0; --j)
            C[j] += C[j - 1];
    
    return C[k];
}

int ValidKnotVector(int *n, int *p, double *U)
{
    /*
    Knot vector check function.
    
    Input: n, p, U
    Output: 0 if check passed, 1 otherwise.
    */
    int i, m;
    
    m = *n + *p + 1; // (m + 1) size of U
    
    for (i = 1; i <= *p; ++i) // Check non-periodicity on left
        if (!CLOSE(U[i], U[0], RTOL, ATOL)) return 1;
    
    for (i = (*p + 1); i <= (*n + 1); ++i) // Check sort
        if (MIOF(U[i], U[i - 1], RTOL, ATOL)) return 1;
    
    for (i = (*n + 1); i < m; ++i) // Check non-periodicity on right
        if (!CLOSE(U[i], U[m], RTOL, ATOL)) return 1;
    
    return 0;
}

void EquallySpaced(int *n, double *x, int *p, double *U)
{
    /*
    Computes the equally spaced knot vector U[0], ..., U[m] with
    m = n + p + 1.
    
    Input: n, x, p, n
        n: the highest index of 'x' array;
        x: the x-coordinates of the data points, must be increasing;
        p: degree of the curve.
    
    Output: U
    
    */
    int j;
    double beta;
    
    beta = x[*n] - x[0];
    
    for (j = 0; j <= *p; ++j)
    {
        U[j] = x[0];    U[*n + *p + 1 - j] = x[*n];
    };
    
    for (j = 1; j <= (*n - *p); ++j)
        U[j + *p] = j*beta/(*n - *p + 1) + x[0];
}

void AveragingAlg1(int *n, double *x, int *p, double *U)
{
    /*
    Computes averaging formula ([2], p. 365) and stores the values in the
    array U[0], ..., U[m] with m = n + p + 1.
    
    Input: n, x, p
        n: the highest index of 'x' array;
        x: the x-coordinates of the data points, must be increasing;
        p: degree of the curve.
    
    Output: U
    
    */
    int i, j;
    double usum;
    
    for (j = 0; j <= *p; ++j)
    {
        U[j] = x[0];
        U[*n + *p + 1 - j] = x[*n];
    };
    
    for (j = 1; j <= (*n - *p); ++j)
    {
        usum = 0.;
        for (i = j; i <= j + *p - 1; ++i)
            usum += x[i];
        U[j + *p] = usum/(*p);
    };
}

void AveragingAlg2(int *n, double *x, int *p, double *U)
{
    /*
    Computes averaging formula ([2], p. 370) and stores the values in the
    array U[0], ..., U[m] with m = n + p + 3.
    
    Input: n, x, p
        n: the highest index of 'x' array;
        x: the x-coordinates of the data points, must be increasing;
        p: degree of the curve.
    
    Output: U
    
    */
    int i, j;
    double usum;
    
    for (j = 0; j <= *p; ++j)
    {
        U[j] = x[0];
        U[*n + *p + 3 - j] = x[*n];
    };
    
    for (j = 0; j <= (*n - *p + 1); ++j)
    {
        usum = 0.;
        for (i = j; i <= j + *p - 1; ++i)
            usum += x[i];
        U[j + *p + 1] = usum/(*p);
    };
}

void AveragingAlg3(int *n, double *x, int *p, int *k, int *l, double *U)
{
    /*
    Computes averaging formula ([7], p. 75) and stores the values in the
    array U[0], ..., U[n + k + l + p + 1].
    
    Input: n, x, p, k, l
        n: the highest index of 'x' array;
        x: the x-coordinates of the data points, must be increasing;
        p: degree of the curve;
        k: number of derivative constraints at left end;
        l: number of derivative constraints at right end.
    
    Output: U
    */
    int i, j, r;
    int is, ie, js, je, m;
    double usum;
    
    m = *n + *k + *l;
    
    for (i = 0; i <= *p; ++i)
    {
        U[i] = x[0];
        U[m + i + 1] = x[*n];
    };
    
    is = 1 - *k;    ie = *n - *p + *l;
    r = *p;
    
    for (i = is; i <= ie; ++i)
    {
        js = MAX(0, i);     je = MIN(*n, i + *p - 1);
        r++;
        usum = 0.;
        for (j = js; j <= je; ++j)
            usum += x[j];
        U[r] = usum/(je - js + 1);
    };
}

void KnotsEvalL2Approx(int *m, double *x, int *p, int *n, double *U)
{
    /*
    Calculates the nodal vector with (n - p) internal nodes according to the
    equation:
        
        | i = int(j*d)    ,   alpha = j*d - i
        |                                                     j= 1, ..., n - p
        | u_(p + j) = (1.0 - alpha) * x(i - 1) + alpha * u(i)
    
    with:         m + 1
            d = ---------
                n - p + 1
    
    Input: m, x, p, n
        m: the highest index of 'x' array;
        x: the x-coordinates of the data points, must be increasing;
        p: degree of the curve;
        n: the highest index of control points (the number of control points
           is n + 1).
    
    Output: U
    
    */
    int i, j;
    double d, alpha;
    
    for (i = 0; i <= *p; ++i)
    {
        U[i] = x[0];
        U[*n + *p + 1 - i] = x[*m];
    };
    
    d = (double)(*m + 1)/(double)(*n - *p + 1);
    
    for (j = 1; j <= (*n - *p); ++j)
    {
        i = (int)(j*d);
        alpha = (double)j*d - (double)i;
        U[*p + j] = (1.0 - alpha)*x[i - 1] + alpha*x[i];
    };
}

void AveragingCpts(int *n, int *p, double *U, double *C, int *info)
{
    /*
    Computes averaging formula ([1], p. 133) and stores the values in the
    array C[0], ..., C[n].
    This function is used for the calculation of the coordinates of spline
    functions' control points as points P(j) = (cpx(j), cpy(j)), where:
    
                  u(j + 1) + ... + u(j + p)
        cpx(j) = ---------------------------         j = 0, ..., n - 1
                              p
    
    Thus:
         x = SUM (cpx(j) * N(j,p)(x) : j = 0, ..., n - 1)
        
         f(x) = SUM (cpy(j) * N(j,p)(x) : j = 0, ..., n - 1)
    
    Input: n, p, U
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform).
    
    Output: C, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j;
    double usum;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    };
    
    if (*info){ return; };
    
    /* Compute the algorithm */
    
    for (i = 0; i <= *n; ++i)
    {
        usum = 0.;
        for (j = 1; j <= *p; ++j)
            usum += U[i + j];
        C[i] = usum / *p;
    };
}

int FindSpan(int *n, int *p, double *u, double *U)
{
    /*
    Determines the knot span index ([2], pp. 67-68).
    
    Input: n, p, u, U
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the basis functions;
        u: independent variable. Must be u(0) <= u < u(m) ;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform). Must be:
            
                u(0) = ... = u(p) = a   &   u(m - p) = ... = u(m) = b
                
                U = {a, ..., a, u(p + 1), ..., u(m - p - 1), b, ..., b}
                     ---------                               ---------
                      (p + 1)                                 (p + 1)
           
           besides, the degree, p, number of control points, n + 1, and number
           of knots, m + 1, are related by:     m = n + p + 1
    
    Output: the knot span index.
    */
    int low, high, mid;
    
    if (CLOSE(*u, U[*n + 1], RTOL, ATOL)) // Special case u = u(m)
        return (*n); 
    
    low = *p;   high = *n + 1; // Do binary search
    mid = (low + high)/2;
    
    while (MIOF(*u, U[mid], RTOL, ATOL) || GREQ(*u, U[mid + 1], RTOL, ATOL))
    {
        if (MIOF(*u, U[mid], RTOL, ATOL))   high = mid;
            else    low = mid;
        mid = (low + high)/2;
    };
    
    return (mid);
}

void FindSpanMult(int *n, int *p, double *u, double *U, int *k, int *s)
{
    /*
    Determines the knot span index, k, and the multiplicity, s.
    
    Input: n, p, u, U
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the basis functions;
        u: independent variable. Must be u(0) <= u < u(m) ;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform).
    
    Output: k, s
    */
    *k = FindSpan(n, p, u, U);
    *s = 0;
    while (CLOSE(*u, U[*k - *s], RTOL, ATOL)) *s += 1;
}

void BasisFuns(int *i, double *u, int *p, double *U, double *left,
               double *right, double *N)
{
    /*
    Computes the nonvanishing basis functions and stores them in the array
    N[0], ..., N[p]. We assume u is in i-th span [u(i), u(i + 1)).
    
    The recurrence relation is used
    
                   u - u(i)                      u(i+p+1) - u
    N(i,p)(u) = --------------- N(i,p-1)(u) + ------------------- N(i+1,p-1)(u)
                 u(i+p) - u(i)                 u(i+p+1) - u(i+1)
    
    with:           
                    | 1 if u(i) <= u < u(i+1)
        N(i,0)(u) = |
                    | 0 otherwise
    
    We introduce the notation
        
        left[j] = u - u(i+1-j)   ;   right[j] = u(i+j) - u      j = 1, ..., p
    
    For algorithm details, see ([1], pp. 109-112)([2], pp. 68-71).
    
    Input: i, u, p, U, left, right
        i: knot span index (we assume u is in i-th span (u(i), u(i + 1)]);
        u: indipendent variable;
        p: degree of the basis functions;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        left: local array of length (p + 1) used by the algorithm;
        right: as 'left'.
    
    Output: N
    */
    int j, r;
    double saved, temp;
    
    N[0] = 1.;
    
    for (j = 1; j <= *p; ++j)
    {
        left[j] = *u - U[*i + 1 - j];
        right[j] = U[*i + j] - *u;
        saved = 0.;
        
        for (r = 0; r < j; ++r)
        {
            temp = N[r]/(right[r + 1] + left[j - r]);
            N[r] = saved + right[r + 1]*temp;
            saved = left[j - r]*temp;
        };
        
        N[j] = saved;
    };
}

void OneBasisFun(int *p, int *m, double *U, int *i, double *u, double *N,
                 double *Nip)
{
    /*
    Compute the basis function Nip ([2], pp. 74-75). This algorithm compute a
    single basis function N_(i, p)(u). The solution to that problem result in
    triangular tables of the form:
    
            N_(i, 0)
                                N_(i, 1)
            N_(i + 1, 0)                            N_(i, 2)
            
                ...                                   ...           N_(i, p)
            
            N_(i + p - 1, 0)                        N_(i + p - 2)
                                N_(i + p - 1, 1)
            N_(i + p, 0)
    
    The algorithm computes only nonzero etries and the value N_(i, p)(u) is
    returned in Nip.
    
    Input: p, m, U, i, u, N
        p: degree of the curve;
        m: the highest index of knot vector;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        i: knot span index;
        u: indipendent variable;
        N: memory allocation of (p + 1) double elements {N(0), ..., N(p)}.
    
    Output: Nip
    
    */
    int j, k;
    double saved, Uleft, Uright, temp;
    
    if ((*i == 0 && CLOSE(*u, U[0], RTOL, ATOL)) ||             /* Special */
        (*i == *m - *p - 1 && CLOSE(*u, U[*m], RTOL, ATOL)))    /*  cases  */
        { *Nip = 1.0; return; };
    
    if (*u < U[*i] || GREQ(*u, U[*i + *p + 1], RTOL, ATOL))/* Local property */
        { *Nip = 0.0; return; };
    
    for (j = 0; j <= *p; ++j)   /* Initialize zeroth-degree functs */
    {
        if (GREQ(*u, U[*i + j], RTOL, ATOL) && *u < U[*i + j + 1])  N[j] = 1.0;
            else        N[j] = 0.0;
    };
    
    for (k = 1; k <= *p; ++k)   /* Compute triangular table */
    {   
        if (CLOSE(N[0], 0.0, RTOL, ATOL))     saved = 0.0;
            else    saved = ((*u - U[*i])*N[0])/(U[*i + k] - U[*i]);
        for (j = 0; j < *p - k + 1; ++j)
        {
            Uleft = U[*i + j + 1];  Uright = U[*i + j + k + 1];
            if (CLOSE(N[j + 1], 0.0, RTOL, ATOL))
            {
                N[j] = saved;   saved = 0.0;
            }
            else
            {
                temp = N[j + 1]/(Uright - Uleft);
                N[j] = saved + (Uright - *u)*temp;
                saved = (*u - Uleft)*temp;
            };
        };
    };
    
    *Nip = N[0];
}

void CurvePoint(int *n, int *p, double *U, double *P, double *u, double *C,
                int *info)
{
    /*
    Computes curve point ([2], pp. 81-82).
    
    Input: n, p, U, P, u
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        u: indipendent variable. Must be u(0) <= u <= u(m).
    
    Output: C, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i;
    int span;
    double *N, *left, *right;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((*u < U[0]) || (*u > U[*n + *p + 1])){
        *info = -5;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    N = (double*) malloc((*p + 1)*sizeof(double));
    if (N == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    left = (double*) malloc((*p + 1)*sizeof(double));
    if (left == NULL)
    {
        free(N);
        *info = MEM_ERR;
        return;
    };
    
    right = (double*) malloc((*p + 1)*sizeof(double));
    if (right == NULL)
    {
        free(N);
        free(left);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    span = FindSpan(n, p, u, U);
    BasisFuns(&span, u, p, U, left, right, N);
    
    *C = 0.;
    for (i = 0; i <= *p; ++i)
        *C += N[i]*P[span - *p + i];

    free(N);
    free(left);
    free(right);
}

void CurveEval(int *n, int *p, double *U, double *P, double *C, int *np,
               int *info)
{
    /*
    Computes curve points for a series of x-coordinates, C. The C vector is
    overwritten with the output values, you need to make a copy.
    
    Input: n, p, U, P, C, np
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        C: on entry, x-coordinates array {x(0), ..., x(np)}. Must be in
           strictly increasing order, x(0) >= U[0] and x(np) <= U[m];
        np: the highest index of C vector.
    
    Output: C, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j;
    int span;
    double *N, *left, *right;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((C[0] < U[0]) || (C[*np] > U[*n + *p + 1])){
        *info = -5;
    } else if (*np < 0){
        *info = -6;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    N = (double*) malloc((*p + 1)*sizeof(double));
    if (N == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    left = (double*) malloc((*p + 1)*sizeof(double));
    if (left == NULL)
    {
        free(N);
        *info = MEM_ERR;
        return;
    };
    
    right = (double*) malloc((*p + 1)*sizeof(double));
    if (right == NULL)
    {
        free(N);
        free(left);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    for (j = 0; j <= *np; ++j)
    {
        span = FindSpan(n, p, &C[j], U);
        BasisFuns(&span, &C[j], p, U, left, right, N);
        
        C[j] = 0.;
        for (i = 0; i <= *p; ++i)
            C[j] += N[i]*P[span - *p + i];
    };
    
    free(N);
    free(left);
    free(right);
}

void DersBasisFuns(int *i, double *u, int *p, int *n, double *U, double *ndu,
                   double *a, double *left, double *right, double *ders)
{
    /*
    Computes the nonzero basis functions and their derivatives, up to and
    including the nth derivative (n <= p). Output is in the two-dimensional
    array, ders. ders[k][j] is the kth derivative of the function N(i-p+j, p),
    where 0 <= k <= n and 0 <= j <= p.
    
    The following relation is used ([2], p. 61):
    
         k            p!
        N(i, p) = ---------- * SUM (a(k, j) * N(i + k, p - k) : j = 0, ..., k)
                   (p - k)!
    
    with:
        a(0, 0) = 1
                        a(k - 1, 0)
        a(k, 0) = -------------------------
                   u(i + p - k + 1) - u(i)
    
                    a(k - 1, j) - a(k - 1, j - 1)
        a(k, j) = ---------------------------------         j = 0, ..., k - 1
                   u(i + p + j - k + 1) - u(i + j)
        
                      - a(k - 1, k - 1)
        a(k, k) = -------------------------
                   u(i + p + 1) - u(i + k)
    
    Two local arrays are used:
    - ndu[p + 1][p + 1], to store the basis function and knot difference. The
      basis functions fit into the upper triangle (including the diagonal), and
      the knot differences fit into the lower triangle, that is:
      
              | N(i, 0)(u)      | N(i-1, 1)(u)  | N(i-2, 2)(u) |
              |-----------------|---------------|--------------|
              | u(i+1) - u(i)   | N(i, 1)(u)    | N(i-1, 2)(u) |
              |-----------------|---------------|--------------|
              | u(i+1) - u(i-1) | u(i+2) - u(i) | N(i, 2)(u)   |
    
    - a[2][p + 1], to store (in an alternating fashion) the two most recently
      computed rows a(k, j) and a(k-1, j).
    
    For algorithm details, see ([2], pp.70-74).
    
    Input: i, u, p, n, k, U
        i: knot span index (we assume u is in i-th span [u(i), u(i + 1)));
        u: indipendent variable;
        p: degree of the curve;
        n: the highest derivative order calculated;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        ndu: see above;
        a: see above;
        left: local array of length (p + 1) used by the algorithm;
        right: as 'left'.
    
    Output: ders
    */
    
    int j, r, k;
    int rk, pk, j1, j2, s1, s2;
    double saved, temp, d;
    const int M = (*p + 1);
    
    ndu[MTX2D(0, 0, M)] = 1.;
    
    for (j = 1; j <= *p; ++j)
    {
        left[j] = *u - U[*i + 1 - j];
        right[j] = U[*i + j] - *u;
        saved = 0.;
        
        for (r = 0; r < j; ++r)
        {   /* Lower triangle */
            
            ndu[MTX2D(j, r, M)] = right[r + 1] + left[j - r];
            temp = ndu[MTX2D(r, (j - 1), M)]/ndu[MTX2D(j, r, M)];
            
            /* Upper triangle */
            
            ndu[MTX2D(r, j, M)] = saved + right[r + 1]*temp;
            saved = left[j - r]*temp;
        };
        
        ndu[MTX2D(j, j, M)] = saved;
    };
    
    for (j = 0; j <= *p; ++j) // Load the basis functions
        { ders[MTX2D(0, j, M)] = ndu[MTX2D(j, *p, M)]; };
    
    /* This section computes the derivatives */
    for (r = 0; r <= *p; ++r) // Loop over function index
    {
        s1 = 0; s2 = 1; // Alternative rows in array a
        a[MTX2D(0, 0, M)] = 1.;
        
        /* Loop to compute kth derivative */
        for (k = 1; k <= *n; ++k)
        {
            d = 0.;
            rk = r - k; pk = *p - k;
            if (r >= k)
            {
                a[MTX2D(s2, 0, M)] = a[MTX2D(s1, 0, M)]/
                                     ndu[MTX2D((pk + 1), rk, M)];
                d = a[MTX2D(s2, 0, M)]*ndu[MTX2D(rk, pk, M)];
            };
            
            if (rk >= -1)   j1 = 1;
                else        j1 = -rk;
            if (r - 1 <= pk)    j2 = k - 1;
                else            j2 = *p - r;
            
            for (j = j1; j <= j2; ++j)
            {
                a[MTX2D(s2, j, M)] = (a[MTX2D(s1, j, M)] -
                a[MTX2D(s1, (j - 1), M)])/ndu[MTX2D((pk + 1), (rk + j), M)];
                d += a[MTX2D(s2, j, M)]*ndu[MTX2D((rk + j), pk, M)];
            };
            
            if (r <= pk)
            {
                a[MTX2D(s2, k, M)] = - a[MTX2D(s1, (k - 1), M)]/
                                     ndu[MTX2D((pk + 1), r, M)];
                d += a[MTX2D(s2, k, M)] * ndu[MTX2D(r, pk, M)];
            };
            
            ders[MTX2D(k, r, M)] = d;
            j = s1; s1 = s2; s2 = j; // Switch rows
        };
    };
    
    /* Multiply through by the correct factors*/
    r = *p;
    for(k = 1; k <= *n; ++k)
    {
        for (j = 0; j <= *p; ++j) ders[MTX2D(k, j, M)] *= r;
        r *= (*p - k);
    };
}

void CurveDerivsAlg1(int *n, int *p, double *U, double *P, double *u, int *d,
                     double *CK, int *info)
{
    /*
    Computes curve derivatives ([2], p. 93) and stores them in the array
    CK[0], ..., CK[d].
    
    Input: n, p, U, P, u, d
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        u: indipendent variable;
        d: the highest derivative order calculated;
    
    Output: CK, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int j, k;
    double *nders;
    double *left, *right;
    double *ndu, *a;
    int du, span;
    const int M = (*p + 1);
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((*u < U[0]) || (*u > U[*n + *p + 1])){
        *info = -5;
    } else if (*d < 0){
        // values ​​of d > p are allowed. In this case kth derivative with k > p
        // is set to 0.
        *info = -6;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    nders = (double*) malloc((MAX((*d + 1), M))*M*sizeof(double));
    if (nders == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    left = (double*) malloc(M*sizeof(double));
    if (left == NULL)
    {
        free(nders);
        *info = MEM_ERR;
        return;
    };
    
    right = (double*) malloc(M*sizeof(double));
    if (right == NULL)
    {
        free(nders);
        free(left);
        *info = MEM_ERR;
        return;
    };
    
    ndu = (double*) malloc(M*M*sizeof(double));
    if (ndu == NULL)
    {
        free(nders);
        free(left);
        free(right);
        *info = MEM_ERR;
        return;
    };
    
    a = (double*) malloc(2*M*sizeof(double));
    if (a == NULL)
    {
        free(nders);
        free(left);
        free(right);
        free(ndu);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    du = MIN(*d, *p);
    for (k = M; k <= *d; ++k) CK[k] = 0.;
    
    span = FindSpan(n, p, u, U);
    DersBasisFuns(&span, u, p, &du, U, ndu, a, left, right, nders);
    
    for (k = 0; k <= du; ++k)
    {
        CK[k] = 0.;
        for (j = 0; j <= *p; ++j)
            CK[k] += nders[MTX2D(k, j, M)]*P[span - (*p) + j];
    };
    
    free(nders);
    free(left);
    free(right);
    free(ndu);
    free(a);
}

void CurveDerivsEval(int *n, int *p, double *U, double *P, int *r1, int *r2,
                     int *np, double *C, int *cp, double *CK, int *info)
{
    /*
    Computes curve derivatives for a series of x-coordinates, C, end stores
    them in the array CK[k][i]. On output, CK[k][i] is the ith value of the
    j-th derivative curve, where j = k + r1. If r1 = 0 and r2 = n, all
    derivative are computed. Values ​​of r2 > p are allowed; in this case kth
    derivative with k > p is set to 0.
    
    For example, let   p = 3, np = 5, r1 = 0, r2 = 4
    
    the CK array looks like:
    
        CK = [ C(0)(0)   C(0)(1)   C(0)(2)   C(0)(3)   C(0)(4)
               C(1)(0)   C(1)(1)   C(1)(2)   C(1)(3)   C(1)(4)
               C(2)(0)   C(2)(1)   C(2)(2)   C(2)(3)   C(2)(4)
                  0.        0.        0.        0.        0.   ]
    
    Input: n, p, U, P, d, C, np
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        r1: minimum derivative order calculated;
        r2: maximum derivative order calculated;
        np: the highest index of C vector;
        C: indipendent variables {x(0), ..., x(np)}. Must be in strictly
           increasing order, x(0) >= U[0] and x(np) <= U[m];
        cp: the highest index of CK vector's rows;
    
    Output: CK, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j, k;
    double *nders;
    double *left, *right;
    double *ndu, *a;
    int du, r, span;
    const int M = (*p + 1);
    const int N = (*np + 1);
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if (*r1 < 0){
        *info = -5;
    } else if (*r2 < *r1){
        // values ​​of r2 > p are allowed. In this case kth derivative with k > p
        // is set to 0.
        *info = -6;
    } else if (*np < 0){
        *info = -7;
    } else if ((C[0] < U[0]) || (C[*np] > U[*n + *p + 1])){
        *info = -8;
    } else if (*cp != (*r2 - *r1)){
        *info = -9;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    nders = (double*) malloc(M*M*sizeof(double));
    if (nders == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    left = (double*) malloc(M*sizeof(double));
    if (left == NULL)
    {
        free(nders);
        *info = MEM_ERR;
        return;
    };
    
    right = (double*) malloc(M*sizeof(double));
    if (right == NULL)
    {
        free(nders);
        free(left);
        *info = MEM_ERR;
        return;
    };
    
    ndu = (double*) malloc(M*M*sizeof(double));
    if (ndu == NULL)
    {
        free(nders);
        free(left);
        free(right);
        *info = MEM_ERR;
        return;
    };
    
    a = (double*) malloc(2*M*sizeof(double));
    if (a == NULL)
    {
        free(nders);
        free(left);
        free(right);
        free(ndu);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    r = *r2 - *r1;
    du = MIN(*r2, *p);
    
    for (i = 0; i <= *np; ++i)
    {
        span = FindSpan(n, p, &C[i], U);
        DersBasisFuns(&span, &C[i], p, &du, U, ndu, a, left, right, nders);
        for (k = 0; k <= r; ++k)
        {
            CK[MTX2D(k, i, N)] = 0.; if ((k + *r1) > *p){ continue; };
            for (j = 0; j <= *p; ++j)
                CK[MTX2D(k, i, N)] += nders[MTX2D((k + *r1), j, M)]*
                                      P[span - (*p) + j];
        };
    };
    
    free(nders);
    free(left);
    free(right);
    free(ndu);
    free(a);
}

void CurveDerivCptsAlg1(int *n, int *p, double *U, double *P, int *d, int *r1,
                        int *r2, double *PK, int *info)
{
    /*
    Computes the control points of all derivative curves up to and including
    the dth derivative (d <= p) and stores them in the array PK[d + 1][n + 1].
    On output, PK[k][i] is the ith control point of the kth derivative curve,
    where 0 <= k <= d and r1 <= i <= (r2 - k). If r1 = 0 and r2 = n, all
    control points are computed.
    
    For example, let   d = 2, p = 3, n = 6, r1 = 2, r2 = 6
    
    the PK array looks like:
    
        PK = [ P(0)(2)   P(0)(3)   P(0)(4)   P(0)(5)   P(0)(6)
               P(1)(2)   P(1)(3)   P(1)(4)   P(1)(5)      -
               P(2)(2)   P(2)(3)   P(2)(4)      -         -   ]
    
    where the elements merked - in the lower right corner are not referenced by
    the routine.
    
    The following relation is used ([2], pp. 97-99):
    
               | P(i)   if k = 0
         k     |
        P(i) = |        p - k + 1            k-1        k-1
               | ------------------------- (P(i + 1) - P(i))  if k > 0
               |  u(i + p + 1) - u(i + k)
    
    Input: n, p, U, d, r1, r2
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        d: the highest derivative order calculated;
        r1: extreme left index of control points computed by the algorithm;
        r2: as r1, but right index (see above).
    
    Output: PK, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, k;
    int r, tmp;
    const int M = (*n + 1);
        
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((*d < 0) || (*d > *p)){
        *info = -5;
    } else if (*r1 < 0 || *r1 > *n){
        *info = -6;
    } else if (*r2 < *r1 || *r2 > *n){
        *info = -7;
    };
    
    if (*info){ return; };
    
    /* Compute the algorithm */
    
    r = *r2 - *r1;
    for (i = 0; i <= r; ++i)
        PK[MTX2D(0, i, M)] = P[*r1 + i];
     
    for (k = 1; k <= *d; ++k)
    {
        tmp = *p - k + 1;
        for (i = 0; i <= (r - k); ++i)
        {
            if (U[*r1 + i + *p + 1] == U[*r1 + i + k])
                { *info = DIV_ZERO_ERR; return; };
            
            PK[MTX2D(k, i, M)] = tmp*(PK[MTX2D((k - 1), (i + 1), M)] - 
              PK[MTX2D((k - 1), i, M)])/(U[*r1 + i + *p + 1] - U[*r1 + i + k]);
        };
    };
}

void CurveKnotIns(int *np, int *p, double *UP, double *P, double *u, int *k,
                  int *s, int *r, int *nq, double *UQ, double *Q, int *info)
{
    /*
    Compute new curve from knot insertion ([2], pp. 141-151). We suppose u in
    [u(k), u(k + 1)) initially has multiplicity 's', and suppose it is to be
    inserted 'r' times, where (r + s) <= p (it generally makes no pratical
    sense to have interior knot multiplicities greater than p). Denote the ith
    new control point in the rth insertion step by Q(i)(r) (with Q(i)(0) = P(i)
    ). Then Q(i)(r) is:
    
        Q(i)(r) = alpha(i)(r)*Q(i)(r-1) + (1 - alpha(i)(r))*Q(i-1)(r-1)
    
    where
                      | 1   if i <= k - p + r - 1
                      |
                      |         u - u(i)
        alpha(i)(r) = | -------------------------   if k - p + r <= i <= k - s
                      |  u(i + p - r + 1) - u(i)
                      |
                      | 0   if i >= k - s + 1
    
    Input: np, p, UP, P, u, k, s, r
        np: the highest index of control points before knot insertion (the
            number of control points is np + 1);
        p: degree of the curve;
        UP: knot vector before knot insertion {u(0), ..., u(np)};
        P: control points before knot insertion;
        u: knot to insert;
        k: knot span index (we assume u is in kth span [u(k), u(k + 1)));
        s: 'u' initial multiplicity;
        r: number of times the knot must be inserted. The final multiplicity
           of 'u' will be (s + r).
    
    Output: nq, UQ, Q
        nq: the highest index of control points after knot insertion, equal to
            np + r (the number of control points is nq + 1);
        UQ: knot vector after knot insertion {u(0), ..., u(nq)};
        Q: control points after knot insertion.
    
    Note: The user must respect the relation:   mp = np + p + 1, with mp the
    highest index of knot vector (mp + 1, lenght of UP array). The same for QP,
    mq and nq, respectively.
    */
    int i, j;
    int mp, L = 0;
    double alpha;
    double *R;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*np < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that np >= p. If p = np, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(np, p, UP)){
        *info = -3;
    } else if ((*u < UP[0]) || (*u > UP[*np + *p + 1])){
        *info = -5;
    } else if ((*k < 0) || (*k > *np)){
        *info = -6;
    } else if ((*s < 0) || (*s > *p)){
        *info = -7;
    } else if ((*r <= 0) || (*r > (*p - *s))){
        *info = -8;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    R = (double*) malloc((*p + 1)*sizeof(double));
    if (R == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    mp = *np + *p + 1;
    *nq = *np + *r;
    
        /* Load new knot vector */
    for (i = 0; i <= *k; ++i) UQ[i] = UP[i];
    for (i = 1; i <= *r; ++i) UQ[*k + i] = *u;
    for (i = (*k + 1); i <= mp; ++i) UQ[i + *r] = UP[i];
    
        /* Save unaltered control points */
    for (i = 0; i <= (*k - *p); ++i) Q[i] = P[i];
    for (i = (*k - *s); i <= *np; ++i) Q[i + *r] = P[i];
    for (i = 0; i <= (*p - *s); ++i) R[i] = P[*k - *p + i];
    
    for (j = 1; j <= *r; ++j) // Insert the knot r times
    {
        L = *k - *p + j;
        for (i = 0; i <= (*p - j - *s); ++i)
        {
            if (UP[i + *k + 1] == UP[L + i])
                { *info = DIV_ZERO_ERR; return; };
            
            alpha = (*u - UP[L + i])/(UP[i + *k + 1] - UP[L + i]);
            R[i] = alpha*R[i + 1] + (1.0 - alpha)*R[i];
        };
        Q[L] = R[0];
        Q[*k + *r - j - *s] = R[*p - j - *s];
    };
    
    for (i = (L + 1); i < (*k - *s); ++i) // Load remaining control points
        Q[i] = R[i - L];
    
    free(R);
}

void RemoveCurveKnot(int *n, int *p, double *U, double *P, double *u, int *r,
                     int *s, int *num, double *TOL, int *t, int *info)
{
    /*
    Remove knot u (index r) num times ([2], pp. 179-188). This algorithm tries
    to remove the knot 'u' 'num' times, where 1 <= num <= s. It returns 't',
    the actual number of times the knot is removed, and if t > 0 it returns the
    new knot vector and control points. It computes the new control points in
    place, overwriting the old ones (if you want to save them you need to make
    a copy).
    One knot removal results in a curve whose deviation from the original curve
    is less than TOL, on the entire parameter domain.
    
    Input: n, p, U, P, u, r, s, num, TOL
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        u: knot to remove;
        r: knot index (u_(r));
        s: u_(r) initial multiplicity;
        num: number of times the knot must be removed;
        TOL: tolerance. Must be greater than or equal to zero.
    
    Output: t, new knots & ctrl pts in U & P
    */
    int m, ord, fout, last, first, off;
    int k, i, j, ii, jj, remflag;
    double alfi, alfj;
    double *temp;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that np >= p. If p = np, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((*u < U[0]) || (*u > U[*n + *p + 1])){
        *info = -5;
    } else if ((*s < 1) || (*s > *p + 1)){
        *info = -7;
    } else if ((*num < 1) || (*num > *s)){
        *info = -8;
    } else if (*TOL < 0.0){
        *info = -9;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    temp = (double*) malloc(2*(*p + 1)*sizeof(double));
    if (temp == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    m = *n + *p + 1;
    ord = *p + 1;
    fout = (2*(*r) - *s - *p)/2; // First control point out
    last = *r - *s;
    first = *r - *p;
    for (*t = 0; *t < *num; --first, ++last, ++(*t))
    {
        off = first - 1; // Diff in index between temp and P
        temp[0] = P[off];   temp[last + 1 - off] = P[last + 1];
        i = first;  j = last;
        ii = 1;     jj = last - off;
        remflag = 0;
        
        while(j - i > *t)
        {   /* Compute new control points for one removal step */
            alfi = (*u - U[i])/(U[i + ord + *t] - U[i]);
            alfj = (*u - U[j - *t])/(U[j + ord] - U[j - *t]);
            temp[ii] = (P[i] - (1.0 - alfi)*temp[ii - 1])/alfi;
            temp[jj] = (P[j] - alfj*temp[jj + 1])/(1.0 - alfj);
            i++;     ii++;
            j--;     jj--;
        };  /* End of while-loop */
        
        if (j - i < *t){ // Check if knot removable
            if (fabs(temp[ii - 1] - temp[jj + 1]) <= *TOL)
                remflag = 1;
        } else {
            alfi = (*u - U[i])/(U[i + ord + *t] - U[i]);
            if (fabs(P[i] - (alfi*temp[ii + *t + 1] +
                (1.0 - alfi)*temp[ii - 1])) <= *TOL)
                remflag = 1;
        };
        
        if (remflag == 0) // Cannot remove any more knots
            break; // Get out of for-loop
        else
        {   /* Successful removal. Save new cont. pts. */
            i = first;  j = last;
            while(j - i > *t)
            {
                P[i] = temp[i - off]; P[j] = temp[j - off];
                i++; j--;
            };
        };
    }; /* End of for-loop */
    
    free(temp);
    
    if (*t == 0) return;
    
    for (k = *r + 1; k <= m; ++k) U[k - *t] = U[k]; // Shift knots
    j = fout; i = j; // P(j) thru P(i) will be overwritten
    for (k = 1; k < *t; ++k)
        if ((k % 2) == 1) // k modulo 2
            i++;     else    j--;
    for (k = i + 1; k <= *n; ++j, ++k) // Shift
        P[j] = P[k];
}

void RemoveCurveKnots(int *n, int *p, double *U, double *P, double *TOL,
                      int *gap, int *info)
{
    /*
    Remove as many knots as possible from a curve ([4]). Number of knots
    removed is stored in 'gap' value.
    
    Input: n, p, U, P, TOL
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        TOL: tolerance. Must be greater than or equal to zero.
        
    Output: gap, new knots & ctrl pts in U & P
    */
    int m, ord, hispan, t, s, mult, fout, last, first;
    int agap, bgap, off, k, k1, i, j, ii, jj, remflag;
    double hiu, u, alfi, alfj;
    double *temp;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that np >= p. If p = np, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if (*TOL < 0.0){
        *info = -5;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    temp = (double*) malloc(2*(*p + 1)*sizeof(double));
    if (temp == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    m = *n + *p + 1;    ord = *p + 1;
    hispan = m - ord;
    *gap = 0; // Size of the gap
    if (hispan < ord) return; // No interior knots
    hiu = U[hispan];
    
    u = U[ord];     s = ord;
    while (CLOSE(u, U[s + 1], RTOL, ATOL)) s++;
    mult = s - *p;
    fout = (2*s - mult - *p)/2; // First control point out
    last = s - mult;    first = mult;
    bgap = s; // Control-point index before gap
    agap = bgap + 1; // Control-point index after gap
    
    while (1)
    {   /* Loop thru knots; stop when pass hiu */
        for (t = 0; t < mult; first--, last++, t++)
        {   /* Try to remove knot mult times */
            off = first - 1; // diff in index of temp and P
            temp[0] = P[off];   temp[last + 1 - off] = P[last + 1];
            i = first;  j = last;
            ii = first - off;   jj = last - off;
            remflag = 0;
            while(j - i > t)
            {   /* Compute new cont pts for 1 removal step */
                alfi = (u - U[i])/(U[i + ord + *gap + t] - U[i]);
                alfj = (u - U[j - t])/(U[j + ord + *gap] - U[j - t]);
                temp[ii] = (P[i++] - (1.0 - alfi)*temp[ii - 1])/alfi;
                temp[jj] = (P[j--] - alfj*temp[jj + 1])/(1.0 - alfj);
                ii++;   jj--;
            }; // End of while-loop
            
            if (j - i < t){ // Check if knot removable
                if (fabs(temp[ii - 1] - temp[jj + 1]) <= *TOL)
                    remflag = 1;
            } else {
                alfi = (u - U[i])/(U[i + ord + *gap + t] - U[i]);
                if (fabs(P[i] - (alfi*temp[ii + t + 1] +
                    (1.0 - alfi)*temp[ii - 1])) <= *TOL)
                    remflag = 1;
            };
            
            if (remflag == 0) // Cannot remove any more knots
                break; // Get out of for-loop
            else
            {   /* Successful removal. Save new cont. pts. */
                i = first;  j = last;
                while(j - i > t)
                {
                    P[i] = temp[i - off];   P[j] = temp[j - off];
                    i++;    j--;
                };
            };
        }; /* End of for-loop */
        
        if (t > 0)
        {   /* Knots removed. Shift cont pts down */
            j = fout;   i = j; // P_(j) thru P_(i) will be overwritten
            for (k = 1; k < t; k++)
                if (k % 2 == 1) i++;  else j--;
            
            for (k = i + 1; k <= bgap; k++) P[j++] = P[k];
            /* Shift */
        }
        else j = bgap + 1;
        
        // No more knots; get out of while-loop
        if (CLOSE(u, hiu, RTOL, ATOL))
             { *gap += t; break; }
        else
        {   // Go to next knot, shift knots and cont pts down, and reset gaps
            k1 = i = s - t + 1;     k = s + *gap + 1;   u = U[k];
            while (CLOSE(u, U[k], RTOL, ATOL)) U[i++] = U[k++];
            mult = i - k1;  s = i - 1;  *gap += t;
            for (k = 0; k < mult; k++) P[j++] = P[agap++];
            bgap = j - 1;
            fout = (2*s - mult - *p)/2;
            last = s - mult;    first = s - *p;   
        };
    }; // end of while-loop
    
    for (i = hispan + 1, k = i - *gap, j = 1; j <= ord; j++)
        U[k++] = U[i++]; // Shift remaining knots
    
    free(temp);
}

void RemoveCurveKnotWithoutTol(int *n, int *p, double *U, double *P, double *u,
                               int *r, int *s, int *num, int *t, int *info)
{
    /*
    Similar to 'RemoveCurveKnot' but without tolerance check. This is a
    'RemoveCurveKnot' wrapper with the TOL parameter set to infinity.
    
    Input: n, p, U, P, u, r, s, num
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        u: knot to remove;
        r: knot index (u_(r));
        s: u_(r) initial multiplicity;
        num: number of times the knot must be removed;
    
    Output: t, new knots & ctrl pts in U & P
    */
    double TOL = INF;
    RemoveCurveKnot(n, p, U, P, u, r, s, num, &TOL, t, info);  
}

void DegreeElevateCurve(int *n, int *p, double *U, double *P, int *t,
                        double *Uh, int *nh, double *Q, int *info)
{
    /*
    Raises the degree from p to p + t, t >= 1 ([2], pp. 188-209).
    
    Input: n, p, U, P, t
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        t: number of degree elevation times.
    
    Output: Uh, nh, Q
    */
    int i, j, k, tr, kj;
    int m, mh, ph, ph2, mpi;
    int kind, r, a, b, cind, mul, oldr, lbz, rbz;
    int save, s, first, last;
    double inv, ua, ub, numer, den, bet, alf, gam;
    double *bezalfs, *bpts, *ebpts, *Nextbpts, *alfs;
    const int M = (*p + 1);
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if (*t < 1){
        *info = -5;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    bezalfs = (double*) malloc((*p + *t + 1)*M*sizeof(double));
    if (bezalfs == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    bpts = (double*) malloc(M*sizeof(double));
    if (bpts == NULL)
    {
        free(bezalfs);
        *info = MEM_ERR;
        return;
    };
    
    ebpts = (double*) malloc((*p + *t + 1)*sizeof(double));
    if (ebpts == NULL)
    {
        free(bezalfs);
        free(bpts);
        *info = MEM_ERR;
        return;
    };
    
    Nextbpts = (double*) malloc((*p - 1)*sizeof(double));
    if (Nextbpts == NULL)
    {
        free(bezalfs);
        free(bpts);
        free(ebpts);
        *info = MEM_ERR;
        return;
    };
    
    alfs = (double*) malloc((*p - 1)*sizeof(double));
    if (alfs == NULL)
    {
        free(bezalfs);
        free(bpts);
        free(ebpts);
        free(Nextbpts);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    m = *n + *p + 1;
    ph = *p + *t; ph2 = ph/2;
    
        /* Compute Bézier degree elevation coefficients */
    bezalfs[MTX2D(0, 0, M)] = bezalfs[MTX2D(ph, *p, M)] = 1.;
    
    for (i = 1; i <= ph2; ++i)
    {
        inv = 1./Bin(ph, i);
        mpi = MIN(*p, i);
        for (j = MAX(0, i - (*t)); j <= mpi; ++j)
            bezalfs[MTX2D(i, j, M)] = inv*Bin(*p, j)*Bin(*t, i - j);
    };
    
    for (i = ph2 + 1; i <= ph - 1; ++i)
    {
        mpi = MIN(*p, i);
        for (j = MAX(0, i - *t); j <= mpi; ++j)
            bezalfs[MTX2D(i, j, M)] = bezalfs[MTX2D((ph - i), (*p - j), M)];
    };
    
    mh = ph; kind = ph + 1;
    r = -1; a = *p;
    b = *p + 1; cind = 1;
    ua = U[0];
    Q[0] = P[0];
    
    for (i = 0; i <= ph; ++i) Uh[i] = ua;
    for (i = 0; i <= *p; ++i) // Initialize first Bézier seg
        bpts[i] = P[i];
    
    while (b < m) // Big loop thru knot vector
    {
        i = b;
        while (b < m && U[b] == U[b + 1]) b += 1;
        mul = b - i + 1;
        mh = mh + mul + *t;
        ub = U[b];
        oldr = r; r = *p - mul;
            /* Insert knot u(b) r times */
        if (oldr > 0) lbz = (oldr + 2)/2; else lbz = 1;
        if (r > 0) rbz = ph - (r + 1)/2; else rbz = ph;
        if (r > 0)
        {   /* Insert knot to get Bézier segment */
            numer = ub - ua;
            for (k = *p; k > mul; --k)
                alfs[k - mul - 1] = numer/(U[a + k] - ua);
            for (j = 1; j <= r; ++j)
            {
                save = r - j; s = mul + j;
                for (k = *p; k >= s; --k)
                {
                    bpts[k] = alfs[k - s]*bpts[k] +
                              (1. - alfs[k - s])*bpts[k - 1];
                };
                Nextbpts[save] = bpts[*p];
            };
        };  /* End of "insert knot" */
        for (i = lbz; i <= ph; ++i) // Degree elevate Bézier
        {   /* Only points lbz, ..., ph are used below */
            ebpts[i] = 0.;
            mpi = MIN(*p, i);
            for (j = MAX(0, i - *t); j <= mpi; ++j)
                ebpts[i] = ebpts[i] + bezalfs[MTX2D(i, j, M)]*bpts[j];
        };  /* End of degree elevating Bézier */
        if (oldr > 1)
        {   /* Must remove knot u = U[a] oldr times */
            first = kind - 2; last = kind;
            den = ub - ua;
            bet = (ub - Uh[kind - 1])/den;
            for (tr = 1; tr < oldr; ++tr)
            {   /* Knot removal loop */
                i = first; j = last; kj = j - kind + 1;
                while (j - i > tr) /* Loop and compute the new */
                {   /* control points for one removal step */
                    if (i < cind)
                    {
                        alf = (ub - Uh[i])/(ua - Uh[i]);
                        Q[i] = alf*Q[i] + (1. - alf)*Q[i - 1];
                    };
                    if (j >= lbz)
                    {
                        if (j - tr <= kind - ph + oldr)
                        {
                            gam = (ub - Uh[j - tr])/den;
                            ebpts[kj] = gam*ebpts[kj] +
                                        (1. - gam)*ebpts[kj + 1];
                        } else
                        {
                            ebpts[kj] = bet*ebpts[kj] +
                                        (1. - bet)*ebpts[kj + 1];
                        };
                    };
                    i += 1; j -= 1; kj -= 1;
                };
                first -= 1; last += 1;
            };
        };  /* End of removing knot, u = U[a] */
        if (a != (*p)) // Load the knot ua
        {
            for (i = 0; i < ph - oldr; ++i)
                { Uh[kind] = ua; kind += 1; };
        };
        for (j = lbz; j <= rbz; ++j) // Load ctrl pts into Q
            { Q[cind] = ebpts[j]; cind += 1; };
        
        if (b < m)
        {   /* Set up for next pass thru loop */
            for (j = 0; j < r; ++j)         bpts[j] = Nextbpts[j];
            for (j = r; j <= (*p); ++j)     bpts[j] = P[b - (*p) + j];
            a = b; b += 1; ua = ub;
        } else
        {   /* End knot */
            for (i = 0; i <= ph; ++i) Uh[kind + i] = ub;
        };
    };  /* End of while-loop (b < m) */
    *nh = mh - ph - 1;
    
    free(bezalfs);
    free(bpts);
    free(ebpts);
    free(Nextbpts);
    free(alfs);
}

void SolveTridiagonal(int *n, double *Q, double *U, double *P, int *info)
{
    /*
    Solve tridiagonal system for C2 cubic spline ([2], pp. 371-373).
    The algorithm assumes that P[0], P[1], P[n + 1], P[n + 2] are already
    computed and loaded into array P, according to the following functions:
    
        (1)   P[0] = Q[0]
                              U[4]
        (2)   - P[0] + P[1] = ---- * D_0
                               3
                                      1 - U[n + 2]
        (3)   - P[n + 1] + P[n + 2] = ------------ * D_n
                                            3
        (4)   P[n + 2] = Q[n]
    
    where D_0 and D_n are the first derivative vectors at the start point and
    the end point of the curve, respectively.
    
    Input: n, Q, U, P[0], P[1], P[n + 1], P[n + 2]
        n: the highest index of control points (the number of control points
           is n + 1);
        Q: the y-coordinates of the points you want to interpolate
           {q(0), ..., q(n)};
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
    
    Output: P
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i;
    int span, p, m;
    double den;
    double *R, *dd;
    double abc[4], left[4], right[4];
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    p = 3;
    m = *n + 2;
    
    if (*n < 3){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(&m, &p, U)){
        *info = -3;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    R = (double*) malloc((*n + 1)*sizeof(double));
    if (R == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    dd = (double*) malloc((*n + 1)*sizeof(double));
    if (dd == NULL)
    {
        free(R);
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    for (i = 3; i < *n; ++i) R[i] = Q[i - 1];
    
    span = 4;
    BasisFuns(&span, &U[span], &p, U, left, right, abc);
    den = abc[1];
    P[2] = (Q[1] - abc[0]*P[1])/den;
    for (i = 3; i < *n; ++i)
    {
        dd[i] = abc[2]/den;
        span = i + 2;
        BasisFuns(&span, &U[span], &p, U, left, right, abc);
        den = abc[1] - abc[0]*dd[i];
        P[i] = (R[i] - abc[0]*P[i - 1])/den;
    };
    dd[*n] = abc[2]/den;
    span = *n + 2;
    BasisFuns(&span, &U[span], &p, U, left, right, abc);
    den = abc[1] - abc[0]*dd[*n];
    P[*n] = (Q[*n - 1] - abc[2]*P[*n + 1] - abc[0]*P[*n - 1])/den;
    for (i = *n - 1; i >= 2; --i) P[i] -= dd[i + 1]*P[i + 1];
    
    free(R);
    free(dd);
}

void CurveDerivCptsAlg2(int *n, int *p, double *U, double *P, int *d,
                        int *nk, double *UK, double *PK, int *info)
{
    /*
    Computes the control points of the dth derivative curve and stores them in
    the array PK ([1], pp. 115-120).
    
    Input: n, p, U, P, d
        n: the highest index of control points P array (the number of control
           points is n + 1);
        p: degree of the curve to be derived (initial degree). The degree of
           the output curve will be p - d;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        d: derivative order. Must be d <= p.
    
    Output: UK, PK, p, nk, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j;
    int m, mk;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if ((*d < 0) || (*d > *p)){
        *info = -5;
    };
    
    if (*info){ return; };
    
    /* Compute the algorithm */
    
    m = *n + *p + 1;
    mk = m - 2*(*d);
    
    for (i = 0; i <= *n; ++i) PK[i] = P[i];
    for (i = 1; i <= *d; ++i)
    {
        for (j = 0; j <= *n - i; ++j)
        {
            if (U[*p + 1 + j] == U[i + j])
                { *info = DIV_ZERO_ERR; return; };
            
            PK[j] = (PK[j + 1] - PK[j])*(*p - i + 1)/
                (U[*p + 1 + j] - U[i + j]);
        };
    };
    for (i = 0; i <= mk; ++i) UK[i] = U[i + *d];    
    *p -= *d;
    *nk = *n - *d;
}

void CurveAntiDerivCpts(int *n, int *p, double *U, double *P, int *d,
                        int *nk, double *UK, double *PK, int *info)
{
    /*
    Computes the control points of the dth antiderivative curve and stores them
    in the array PK[n + d] ([1], pp. 127-128). This is the inverse function of
    'CurveDerivCptsAlg2'.
    
    Input: n, p, U, P, d
        n: the highest index of control points P array (the number of control
           points is n + 1);
        p: degree of the curve to be integrated (initial degree). The degree of
           the output curve will be p + d;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        d: antiderivative order;
        nk: the highest index of control points PK array.
    
    Output: UK, PK, p, nk, info
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if (*d < 0){
        *info = -5;
    } else if (*nk < *n + *d){
        *info = -6;
    };
    
    if (*info){ return; };
    
    /* Compute the algorithm */
    
    *nk = *n + *d;
    
    for (i = 0; i < *d; ++i)
        { PK[i] = 0.; UK[i] = U[0]; };
    for (i = *d; i <= *nk; ++i)
        { PK[i] = P[i - *d]; UK[i] = U[i - *d]; };
    for (i = *nk + 1; i <= *nk + *p + *d + 1; ++i)
        { UK[i] = U[*n + *p + 1]; };
    
    for (i = 0; i < *d; ++i)
    {
        for (j = *d - i; j <= *nk; ++j) PK[j] *= UK[*p + i + 1 + j] - UK[j];
        for (j = *d - i + 1; j <= *nk; ++j) PK[j] += PK[j - 1];
        for (j = *d - i; j <= *nk; ++j) PK[j] /= (*p + i + 1);
    };
    
    *p += *d;
}

void RefineKnotVectCurve(int *n, int *p, double *U, double *P, double *X,
                         int *r, double *Ubar, double *Q, int *info)
{
    /*
    Refine curve knot vector ([2], pp. 162-167).
    
    Input: n, p, U, P, X, r
        n: the highest index of control points P array (the number of control
           points is n + 1);
        p: degree of the curve to be integrated (initial degree). The degree of
           the output curve will be p + d;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        X: new knots array {x(0), ..., x(r)}. Must be in ascending order.
           New knots x(i) should be repeated in X with their multiplicities;
           e.g., if x and y (x < y) are to be inserted with multiplicities 2
           and 3, respectively, then X = {x, x, y, y, y};
        r: the highest index of X array.
    
    Output: Ubar, Q
    
    Note: The user must respect the relation:   m = n + p + 1, with m the
    highest index of knot vector (m + 1, lenght of U array).
    */
    int i, j, k, l;
    int m, a, b, ind;
    double alfa;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*p < 0){
        *info = -2;   
    } else if (*n < *p){
        // At least p + 1 coefficients are required for a spline of degree p,
        // so that n >= p. If p = n, the curve is a Bezier curve.
        *info = -1;
    } else if (ValidKnotVector(n, p, U)){
        *info = -3;
    } else if (X[0] <= U[0] || X[*r] >= U[*n + *p + 1]){
        *info = -5;
    } else if (*r < 0){
        *info = -6;
    };
    
    if (*info){ return; };
    
    /* Compute the algorithm */
    
    m = *n + *p + 1;
    a = FindSpan(n, p, &X[0], U);
    b = FindSpan(n, p, &X[*r], U);
    b += 1;
    for (j = 0; j <= a - (*p); ++j) Q[j] = P[j];
    for (j = b - 1; j <= *n; ++j) Q[j + *r + 1] = P[j];
    for (j = 0; j <= a; ++j) Ubar[j] = U[j];
    for (j = b + *p; j <= m; ++j) Ubar[j + *r + 1] = U[j];
    i = b + *p - 1;     k = b + *p + *r;
    
    for (j = *r; j >= 0; --j)
    {
        while (X[j] <= U[i] && i > a)
        {
            Q[k - *p - 1] = P[i - *p - 1];
            Ubar[k] = U[i];
            k -= 1; i -= 1;
        };
        
        Q[k - *p - 1] = Q[k - *p];
        
        for (l = 1; l <= *p; ++l)
        {
            ind = k - *p + l;
            alfa = Ubar[k + l] - X[j];
            if (CLOSE(fabs(alfa), 0.0, RTOL, ATOL))
                Q[ind - 1] = Q[ind];
            else
            {
                alfa /= (Ubar[k + l] - U[i - *p + l]);
                Q[ind - 1] = alfa*Q[ind - 1] + (1.0 - alfa)*Q[ind];
            };
        };
        
        Ubar[k] = X[j];
        k -= 1;
    };
}

void IncreaseMultByOne(int *m, int *p, double *U, int *mh, double *Uh)
{
    /*
    Returns the knot vector obtained by degree elevating U from p to p + 1
    (increase all multiplicities by 1).
    
    Input: m, p, U, mh
        m: the highest index of 'U' array;
        p: degree of the basis functions;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        mh: the highest index of 'Uh' array.
    
    Output: Uh
    
    Note: The user must respect the relation: mh = m + s + 2, whit s the number
    of all distinct interior knots.
    */
    int i, j;
    int multflag;
    
    for (i = 0; i <= (*p + 1); ++i)
        { Uh[i] = U[0]; Uh[*mh - *p - 1 + i] = U[*m]; };
    
    multflag = 0;
    j = *p + 1;
    for (i = *p + 2; i <= *mh - *p - 2; ++i)
    {
        Uh[i] = U[j];
        
        if (!CLOSE(U[j + 1], U[j], RTOL, ATOL) && multflag == 0){
            multflag = 1;
        } else {
            multflag = 0;
            ++j;
        };
    };
}

void GetBezierMatrixElement(int *p, int *r, int *c, double *el)
{
    *el =  (
    (double)Bin(*p, *r) * (double)Bin(*r, *c) *
    pow(-1.0, (double)(*r) - (double)(*c)));
}

void GetBezierMatrix(int *p, double *M)
{
    /*
    Calculates the matrix representation of the Bézier curve of degree p with
    the formula:
                                                  | i = 0, ..., p
        Bin(p, i) * Bin(i, k) * (-1)^(i - k) ,    |
                                                  | k = 0, ..., i
    
    Input: p
        p: degree of the curve.
        
    Output: M (an array of size (p + 1)*2)
    
    */
    int i, k;
    
    for (i = 0; i <= *p; ++i)
        for (k = 0; k <= i; ++k)
            GetBezierMatrixElement(p, &i, &k, &M[MTX2D(i, k, *p + 1)]);
}

void BezierProduct(double *fb, int *p, double *gb, int *q, double *M,
                   int *first, int *last, double *hb)
{
    /*
    Given two Bézier functions:
        
        | F(u) = SUM (B_(i, p)(u) * f_(i) : i = 0, ..., p)
        |
        | G(u) = SUM (B_(j, p)(u) * g_(j) : j = 0, ..., q)
    
    their product is computed as follow:
        
        | H(u) = SUM (B_(k, p + q)(u) * h_(k) : k = 0, ..., p + q)
        |
        | h_(k) = SUM ((BIN(p,l) * BIN(q,k-l) * f_(l) * g_(k-l)) / BIN(p+q,k),
        |               l = max(0,k-q),..., min(p,k))
    
    
    Input:
    
    Output: hb
    
    
    */
}

void CurvesProduct()
{
    /*
    Returns the product of two B-splines [5]. Given two B-spline functions
    F(u) and G(u), of degree p and q, respectively, compute the degree p + q
    product fucntion H(u) = F(u) * G(u) defined over the knot vector:
    
        T = {e, ..., e, u_(p + q + 1), ..., u_(n), f, ..., f}
             ---------                             ---------
             p + q + 1                             p + q + 1
    
    The approach used includes:
    
    (1) decompose the B-splines into their Bézier components using knot
        insertion;
    (2) compute the product of the Bézier functions;
    (3) recompose the Bézier product functions into B-spline form using knot
        removal.
    
    
    Input:
    
    Output:
    
    */
}

void Bernstein(int *i, int *n, double *u, double *B, int *info)
{
    /*
    Compute the value of a nth-degree Bernstein polynomial given by:
        
                          n!
        B_(i, n)(u) = ---------- * u^(i) * (1 - u)^(n - i)    with 0 <= u <= 1
                      i!(n - i)!
    
    at fixed value of 'u'.
    
    Input: i, n, u
        i: knot span index;
        n: degree of the Bernstein polynomial;
        u: indipendent variable. Must be 0.0 <= u <= 1.0.
    
    Output: B, info
    */
    int j, k;
    double u1;
    double *temp;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if ((*i < 0) || (*i > *n)){
        *info = -1;
    } else if (*n < 0){
        *info = -2;
    } else if ((*u < 0.0) || (*u > 1.0)){
        *info = -3;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    temp = (double*) malloc((*n + 1)*sizeof(double));
    if (temp == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    for (j = 0; j <= *n; ++j)
        temp[j] = 0.0;
    temp[j] = 1.0;
    
    u1 = 1.0 - *u;
    for (k = 1; k <= *n; ++k)
        for (j = *n; j >= k; --j)
            temp[j] = u1*temp[j] + (*u)*temp[j - 1];
    *B = temp[*n];
    
    free(temp);
}

void AllBernstein(int *n, double *u, double *B)
{
    /*
    Compute all nth-degree Bernstein polynomials.
    
    Input: n, u
        n: degree of the Bernstein polynomial;
        u: indipendent variable. Must be 0.0 <= u <= 1.0.
    
    Output: B (an array, B[0], ..., B[n])
    */
    int j, k;
    double u1, saved, temp;
    
    B[0] = 1.0; u1 = 1.0 - *u;
    for (j = 1; j <= *n; ++j)
    {
        saved = 0.0;
        for (k = 0; k < j; ++k)
        {
            temp = B[k];
            B[k] = saved + u1*temp;
            saved = (*u)*temp;
        };
        B[j] = saved;
    };
}

void PointOnBezierCurve(double *P, int *n, double *u, double *C, int *info)
{
    /*
    Compute point on Bezier curve.
    
    Input: P, n, u
        P: control points {P[0], ..., P[n]};
        n: degree of the curve;
        u: indipendent variable. Must be 0.0 <= u <= 1.0.
    
    Output: C (a point), info
    */
    int k;
    double *B;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*n < 0){
        *info = -2;
    } else if ((*u < 0.0) || (*u > 1.0)){
        *info = -3;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    B = (double*) malloc((*n + 1)*sizeof(double));
    if (B == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    
    AllBernstein(n, u, B);
    *C = 0.0;
    for (k = 0; k <= *n; ++k)
        *C += B[k]*P[k];
    
    free(B);
}

void BezierCurveEval(double *P, int *n, double *C, int *np, int *info)
{
    /*
    Computes Bezier curve points for a series of x-coordinates, C. The C
    vector is overwritten with the output values, you need to make a copy.
    
    Input: P, n, C
        P: control points {P[0], ..., P[n]};
        n: degree of the curve;
        C: on entry, x-coordinates array {x(0), ..., x(np)}. Must be in
           strictly increasing order, 0.0 <= x(i) <= 1.0;
        np: the highest index of C vector.
    
    Output: C, info
    
    */
}

void deCasteljau1(double *P, int *n, double *u, double *C, int *info)
{
    /*
    Compute point on a Bezier curve using deCasteljau.
    
    Input: P, n, u
        P: control points {P[0], ..., P[n]};
        n: degree of the curve;
        u: indipendent variable. Must be 0.0 <= u <= 1.0.
    
    Output: C (a point), info
    */
    int i, k;
    double *Q;
    
    *info = SUCCESS;
    
    /* Test the input parameters */
    
    if (*n < 0){
        *info = -2;
    } else if ((*u < 0.0) || (*u > 1.0)){
        *info = -3;
    };
    
    if (*info){ return; };
    
    /* Local arrays memory allocation */
    
    Q = (double*) malloc((*n + 1)*sizeof(double));
    if (Q == NULL)
    {
        *info = MEM_ERR;
        return;
    };
    
    /* Compute the algorithm */
    for (i = 0; i <= *n; ++i)   Q[i] = P[i];
    for (k = 1; k <= *n; ++k)
        for (i = 0; i <= *n - k; ++i)
            Q[i] = (1.0 - *u)*Q[i] + (*u)*Q[i + 1];
    *C = Q[0];
    
    free(Q);
}

void BezierCurveEval2(double *P, int *n, double *C, int *np, int *info)
{
    /*
    Computes Bezier curve points for a series of x-coordinates, C, using
    deCasteljau. The C vector is overwritten with the output values, you
    need to make a copy.
    
    Input: P, n, C
        P: control points {P[0], ..., P[n]};
        n: degree of the curve;
        C: on entry, x-coordinates array {x(0), ..., x(np)}. Must be in
           strictly increasing order, 0.0 <= x(i) <= 1.0;
        np: the highest index of C vector.
    
    Output: C, info
    
    */
}

void GetRemovalBndCurve(int *n, int *p, double *U, double *P, double *u,
                        int *r, int *s, double *temp, double *Br)
{
    /*
    Get knot removal error bound.

    Input: n, p, U, P, u, r, s, temp
        n: the highest index of control points (the number of control points
           is n + 1);
        p: degree of the curve;
        U: knot vector {u(0), ..., u(m)} (nonperiodic and nonuniform);
        P: control points {c(0), ..., c(n)} (or B-splines coefficients);
        u: knot to remove;
        r: knot index (u_(r));
        s: u_(r) initial multiplicity;
        temp: local array of length (2*p + 1) used by the algorithm;
    
    Output: Br
    */
    int ord, last, first;
    int off;
    int i, j, ii, jj;
    double alfi, alfj;
    
    ord = *p + 1;
    last = *r - *s; 	first = *r - *p;
    off = first - 1; // difference in index between temp and P
    temp[0] = P[off]; 	temp[last + 1 - off] = P[last + 1];
    
    i = first; 	j = last;
    ii = 1; 	jj = last - off;
    
    while (j - i > 0)
    {   /* Compute new control points for one removal step */
        alfi = (*u - U[i])/(U[i + ord] - U[i]);
        alfj = (*u - U[j])/(U[j + ord] - U[j]);
        temp[ii] = (P[i] - (1.0 - alfi)*temp[ii - 1])/alfi;
        temp[jj] = (P[j] - alfj*temp[jj + 1])/(1.0 - alfj);
        
        i++; 	ii++;
        j--; 	jj--;
    }; // End of while-loop
    
    if (j - i < 0){ // now get bound
        *Br = fabs(temp[ii - 1] - temp[jj + 1]); 
    } else {
    	alfi = (*u - U[i])/(U[i + ord] - U[i]);
    	*Br = fabs(P[i] - (alfi*temp[ii + 1] + (1.0 - alfi)*temp[ii - 1]));
    };
}