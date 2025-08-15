import numpy as np

class SplineCubic:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n = len(x) - 1

        self.min_x = np.min(x)
        self.max_x = np.max(x)

        h = x[1:] - x[:-1]

        A = np.zeros((self.n-1, self.n-1))
        B = np.zeros(self.n-1)

        for i in range(1, self.n):
            if i > 1:
                A[i-1, i-2] = h[i-1]
            A[i-1, i-1] = 2 * (h[i-1] + h[i])
            if i < self.n-1:
                A[i-1, i] = h[i]
            B[i-1] = 3 * ((y[i+1] - y[i]) / h[i] - (y[i] - y[i-1]) / h[i-1])

        self.c = np.zeros(self.n+1)
        self.c[1:self.n] = np.linalg.solve(A, B)

        self.a = y[:-1]
        self.b = np.zeros(self.n)
        self.d = np.zeros(self.n)
        for i in range(self.n):
            self.b[i] = (y[i+1] - y[i])/h[i] - h[i]*(2*self.c[i] + self.c[i+1])/3
            self.d[i] = (self.c[i+1] - self.c[i]) / (3*h[i])

    def __call__(self, x_eval):
        if np.isscalar(x_eval):
            x_eval = np.array([x_eval])
            is_scalar = True
        else:
            x_eval = np.asarray(x_eval)
            is_scalar = False

        y_eval = np.zeros_like(x_eval)

        for i in range(self.n):
            mask = (x_eval >= self.x[i]) & (x_eval <= self.x[i+1])
            dx = x_eval[mask] - self.x[i]
            y_eval[mask] = self.a[i] + self.b[i]*dx + self.c[i]*dx**2 + self.d[i]*dx**3

        if is_scalar: return y_eval[0]
        return y_eval