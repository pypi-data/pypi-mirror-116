class SettingsInversion:
    def __init__(
        self,
        use_w_tilde: bool = False,
        use_linear_operators: bool = False,
        tolerance: float = 1e-8,
        maxiter: int = 250,
        check_solution: bool = True,
    ):

        self.use_w_tilde = use_w_tilde
        self.use_linear_operators = use_linear_operators
        self.tolerance = tolerance
        self.maxiter = maxiter
        self.check_solution = check_solution
