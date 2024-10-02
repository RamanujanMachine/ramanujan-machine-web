interface Constant {
	name?: string;
	replacement?: string;
	url?: string;
}

// See https://github.com/RamanujanMachine/LIReC/blob/main/LIReC/lib/calculator.py for each of the following keys
// make sure these are alpha sorted because otherwise e.g. alpha will be replaced instead of alpha_GW
const constants: { [abbrev: string]: Constant } = {
	alpha_GW: { name: 'Goemans Williamson Constant', replacement: 'α[GW]' },
	alpha_M: {
		name: 'Madelung Constant',
		replacement: 'α[M]',
		url: 'https://en.wikipedia.org/wiki/Madelung_constant'
	},
	alpha_F: {
		name: 'Foias Constant',
		replacement: 'α[F]',
		url: 'https://en.wikipedia.org/wiki/Foias_constant'
	},
	alpha: {
		name: 'Second Feigenbaum Constant',
		replacement: 'α',
		url: 'https://en.wikipedia.org/wiki/Feigenbaum_constants#The_second_constant'
	},
	A_Pi: {
		name: 'Mills Constant',
		replacement: 'A[π]',
		url: 'https://en.wikipedia.org/wiki/Mills%27_constant'
	},
	A: {
		name: 'Glaisher Kinkelin Constant',
		url: 'https://en.wikipedia.org/wiki/Glaisher%E2%80%93Kinkelin_constant'
	},
	beta_Levy: {
		name: 'First Lévy Constant',
		replacement: 'β',
		url: 'https://en.wikipedia.org/wiki/L%C3%A9vy%27s_constant'
	},
	beta: {
		name: 'Bernstein Constant',
		replacement: 'β',
		url: 'https://en.wikipedia.org/wiki/Bernstein%27s_constant'
	},
	B_2: {
		name: 'Brun Constant',
		replacement: 'B[2]',
		url: 'https://en.wikipedia.org/wiki/Brun%27s_theorem'
	},
	B_H: {
		name: 'Backhouse Constant',
		replacement: 'B[H]',
		url: 'https://en.wikipedia.org/wiki/Backhouse%27s_constant'
	},
	cbrt2: { replacement: 'cbrt(2)' },
	cbrt3: { replacement: 'cbrt(3)' },
	C_Artin: {
		name: 'Artin Constant',
		replacement: 'C[Artin]',
		url: 'https://en.wikipedia.org/wiki/Artin%27s_conjecture_on_primitive_roots'
	},
	C_HBM: {
		name: 'Heath-Brown–Moroz Constant',
		replacement: 'C[HBM]',
		url: 'https://en.wikipedia.org/wiki/Heath-Brown%E2%80%93Moroz_constant'
	},
	C_CE: {
		name: 'Copeland Erdős Constant',
		replacement: 'C[CE]',
		url: 'https://en.wikipedia.org/wiki/Copeland%E2%80%93Erd%C5%91s_constant'
	},
	C_FT: {
		name: 'Feller Tornier Constant',
		replacement: 'C[FT]',
		url: 'https://en.wikipedia.org/wiki/Feller%E2%80%93Tornier_constant'
	},
	C_10: {
		name: 'Base 10 Champernowne Constant',
		replacement: 'C[10]',
		url: 'https://en.wikipedia.org/wiki/Champernowne_constant'
	},
	C_1: { name: 'First Continued Fraction Constant', replacement: 'C[1]' },
	C_N: {
		name: 'Niven Constant',
		replacement: 'C[N]',
		url: 'https://en.wikipedia.org/wiki/Niven%27s_constant'
	},
	C_P: {
		name: 'Porter Constant',
		replacement: 'C[P]',
		url: 'https://en.wikipedia.org/wiki/Porter%27s_constant'
	},
	C_2: {
		name: 'Second du Bois-Reymond Constant',
		replacement: 'C[2]',
		url: 'https://es.wikipedia.org/wiki/Constante_Du_Bois_Reymond'
	},
	C: { name: 'Catalan Constant', url: 'https://en.wikipedia.org/wiki/Catalan%27s_constant' },
	c: {
		name: 'Asymptotic Lebesgue Constant',
		replacement: 'Λ[n]',
		url: 'https://en.wikipedia.org/wiki/Lebesgue_constant'
	},
	delta_ETF: {
		name: 'Erdős-Tenenbaum-Ford Constant',
		replacement: 'δ[ETF]',
		url: 'https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Tenenbaum%E2%80%93Ford_constant'
	},
	delta_G: {
		name: 'Gompertz Constant',
		replacement: 'δ[G]',
		url: 'https://en.wikipedia.org/wiki/Gompertz_constant'
	},
	Delta_3: {
		name: 'Robbins Constant',
		replacement: '∆(3)',
		url: 'https://en.wikipedia.org/wiki/Mean_line_segment_length#Cube_and_hypercubes'
	},
	delta: {
		name: 'First Feigenbaum Constant',
		replacement: 'δ',
		url: 'https://en.wikipedia.org/wiki/Feigenbaum_constants#The_first_constant'
	},
	D_V: { name: 'Devicci Tesseract Constant', replacement: 'D[V]' },
	D: { name: 'Dottie Number', url: 'https://en.wikipedia.org/wiki/Dottie_number' },
	eLevy: { name: 'Second Lévy Constant', replacement: 'e^β' },
	epi: {
		name: 'Gelfond Constant',
		replacement: 'e^π',
		url: 'https://en.wikipedia.org/wiki/Gelfond%27s_constant'
	},
	E: {
		name: 'Erdos Borwein constant',
		url: 'https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Borwein_constant'
	},
	F: {
		name: 'Fransén Robinson Constant',
		url: 'https://en.wikipedia.org/wiki/Frans%C3%A9n%E2%80%93Robinson_constant'
	},
	gamma: {
		name: 'Euler Mascheroni Constant',
		url: 'https://en.wikipedia.org/wiki/Euler%27s_constant'
	},
	G_025: { replacement: 'Γ(0.25)' },
	G_L: {
		name: 'Gieseking Constant or Lobachevsky Constant',
		replacement: 'G[L]',
		url: 'https://mathworld.wolfram.com/GiesekingsConstant.html'
	},
	G_S: {
		name: 'Gelfond-Schneider Constant or Hilbert Number',
		replacement: '2^sqrt(2)',
		url: 'https://en.wikipedia.org/wiki/Hilbert_number'
	},
	g: { name: 'Golden Angle', url: 'https://en.wikipedia.org/wiki/Golden_angle' },
	G: { name: 'Gauss Constant (ϖ/π)', url: 'https://en.wikipedia.org/wiki/Lemniscate_constant' },
	Kprime: {
		replacement: 'Κ',
		name: 'Kepler Bouwkamp Constant',
		url: 'https://en.wikipedia.org/wiki/Kepler%E2%80%93Bouwkamp_constant'
	},
	K_0: {
		name: 'Khinchin Constant',
		replacement: 'K[0]',
		url: 'https://en.wikipedia.org/wiki/Khinchin%27s_constant'
	},
	lambda_GD: {
		name: 'Golomb Dickman Constant',
		replacement: 'λ[GD]',
		url: 'https://en.wikipedia.org/wiki/Golomb%E2%80%93Dickman_constant'
	},
	lambda_C: {
		name: 'Conway Constant',
		replacement: 'λ[C]',
		url: 'https://en.wikipedia.org/wiki/Look-and-say_sequence#Growth_in_length'
	},
	ln2: { replacement: 'ln(2)' },
	L_lim: {
		name: 'Laplace Limit',
		replacement: 'L[lim]',
		url: 'https://en.wikipedia.org/wiki/Laplace_limit'
	},
	L_Lochs: {
		name: 'Loch Constant',
		replacement: 'L[Lochs]',
		url: 'https://mathworld.wolfram.com/LochsConstant.html'
	},
	L_1: {
		name: 'First Lemniscate Constant (ϖ/2)',
		replacement: 'L[1]',
		url: 'https://en.wikipedia.org/wiki/Lemniscate_constant'
	},
	L_2: {
		name: 'Secnd Lemniscate Constant (π/(2ϖ))',
		replacement: 'L[2]',
		url: 'https://en.wikipedia.org/wiki/Lemniscate_constant'
	},
	L_R: {
		name: 'Landau Ramanujan Constant',
		replacement: 'L[R]',
		url: 'https://en.wikipedia.org/wiki/Landau%E2%80%93Ramanujan_constant'
	},
	L_D: { name: 'Logarithmic Capacity of the Unit Disk', replacement: 'L[D]' },
	L: {
		name: 'Liouville Constant',
		url: "https://en.wikipedia.org/wiki/Liouville_number#The_existence_of_Liouville_numbers_(Liouville's_constant)"
	},
	mu: {
		replacement: 'μ',
		name: 'Hexagonal Lattice Connective Constant',
		url: 'https://en.wikipedia.org/wiki/Connective_constant'
	},
	M: {
		name: 'Meissel Mertens Constant',
		url: 'https://en.wikipedia.org/wiki/Meissel%E2%80%93Mertens_constant'
	},
	Omega: {
		replacement: 'Ω',
		name: 'Omega Constant',
		url: 'https://en.wikipedia.org/wiki/Omega_constant'
	},
	phi: { name: 'Golden Ratio', url: 'https://en.wikipedia.org/wiki/Golden_ratio' },
	psi_Fib: {
		name: 'Reciprocal Fibonacci Constant',
		replacement: 'ψ[Fib]',
		url: 'https://en.wikipedia.org/wiki/Reciprocal_Fibonacci_constant'
	},
	psi: {
		replacement: 'ψ',
		name: 'Super Golden Ratio',
		url: 'https://en.wikipedia.org/wiki/Supergolden_ratio'
	},
	Pi_2: {
		name: 'Twin Primes Constant',
		replacement: 'Π[2]',
		url: 'https://en.wikipedia.org/wiki/Twin_prime'
	},
	P_Dragon: {
		name: 'Paperfolding Constant',
		replacement: 'P[Dragon]',
		url: 'https://en.wikipedia.org/wiki/Regular_paperfolding_sequence#Paperfolding_constant'
	},
	P: {
		name: 'Universal Parabolic Constant',
		url: 'https://en.wikipedia.org/wiki/Universal_parabolic_constant'
	},
	q: {
		name: 'Komornik–Loreti Constant',
		url: 'https://en.wikipedia.org/wiki/Komornik%E2%80%93Loreti_constant'
	},
	root12of2: { replacement: 'nthRoot(2, 12)' },
	rho_Pi: {
		name: 'Prime Constant',
		replacement: 'ρ[Pi]',
		url: 'https://en.wikipedia.org/wiki/Prime_constant'
	},
	rho: {
		name: 'Plastic Number',
		replacement: 'Ρ',
		url: 'https://en.wikipedia.org/wiki/Plastic_ratio'
	},
	R_S: {
		name: 'Ramanujan Soldner Constant',
		replacement: 'R[S]',
		url: 'https://en.wikipedia.org/wiki/Ramanujan%E2%80%93Soldner_constant'
	},
	R: {
		name: 'Ramanujan Constant',
		url: "https://en.wikipedia.org/wiki/Heegner_number#Almost_integers_and_Ramanujan's_constant"
	},
	sigma_10: {
		name: 'Salem Constant',
		replacement: 'σ[10]',
		url: 'https://mathworld.wolfram.com/SalemConstants.html'
	},
	sigma_S: {
		name: 'Somos Quadratic Recurrence Constant',
		replacement: 'σ[S]',
		url: 'https://en.wikipedia.org/wiki/Somos%27_quadratic_recurrence_constant'
	},
	sigma: {
		name: 'Hafner-Sarnak-McCurley Constant',
		replacement: 'σ',
		url: 'https://en.wikipedia.org/wiki/Hafner%E2%80%93Sarnak%E2%80%93McCurley_constant'
	},
	sqrt2: { replacement: 'sqrt(2)' },
	sqrt3: { replacement: 'sqrt(3)' },
	S_MRB: {
		name: 'MRB Constant',
		replacement: 'S[MRB]',
		url: 'https://en.wikipedia.org/wiki/MRB_constant'
	},
	S_Pi: {
		name: 'Stephens Constant',
		replacement: 'S[Pi]',
		url: 'https://en.wikipedia.org/wiki/Stephens%27_constant'
	},
	S: {
		name: 'Sierpiński Constant',
		url: 'https://en.wikipedia.org/wiki/Sierpi%C5%84ski%27s_constant'
	},
	theta_m: {
		name: 'Magic Angle',
		replacement: 'θ[m]',
		url: 'https://en.wikipedia.org/wiki/Magic_angle'
	},
	tau: {
		name: 'Prouhet Thue Morse Constant',
		replacement: 'τ',
		url: 'https://en.wikipedia.org/wiki/Prouhet%E2%80%93Thue%E2%80%93Morse_constant'
	},
	T_Pi: {
		name: 'Taniguchi Constant',
		replacement: 'T[Pi]',
		url: 'https://mathworld.wolfram.com/TaniguchisConstant.html'
	},
	T: {
		name: 'Tribonacci Constant',
		replacement: 'η',
		url: 'https://en.wikipedia.org/wiki/Generalizations_of_Fibonacci_numbers#Tribonacci_numbers'
	},
	V_dp: {
		name: 'Van der Pauw Constant',
		replacement: 'π/ln(2)',
		url: 'https://en.wikipedia.org/wiki/Van_der_Pauw_method#Calculating_sheet_resistance'
	},
	V: {
		name: 'Viswanath Constant',
		url: 'https://en.wikipedia.org/wiki/Random_Fibonacci_sequence'
	},
	W_S: {
		name: 'Weierstrass Constant',
		replacement: 'W[S]',
		url: 'https://mathworld.wolfram.com/WeierstrassConstant.html'
	},
	W: { name: 'Wallis Constant', url: 'https://mathworld.wolfram.com/WallissConstant.html' },
	Zeta2: {
		replacement: 'ζ(2)',
		name: 'Riemann Zeta Function',
		url: 'https://en.wikipedia.org/wiki/Riemann_zeta_function'
	},
	Zeta3: {
		replacement: 'ζ(3)',
		name: 'Apery Constant',
		url: 'https://en.wikipedia.org/wiki/Ap%C3%A9ry%27s_constant#Irrational_number'
	},
	z_975: {
		name: 'Z Score for 97.5 Percentile Point',
		replacement: 'z[97.5]',
		url: 'https://en.wikipedia.org/wiki/97.5th_percentile_point'
	}
};

export default constants;
