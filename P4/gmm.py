import numpy as np
from kmeans import KMeans

class GMM():
    '''
        Fits a Gausian Mixture model to the data.

        attrs:
            n_cluster : Number of mixtures (Int)
            e : error tolerance (Float) 
            max_iter : maximum number of updates (Int)
            init : initialization of means and variance
                Can be 'random' or 'kmeans' 
            means : means of Gaussian mixtures (n_cluster X D numpy array)
            variances : variance of Gaussian mixtures (n_cluster X D X D numpy array) 
            pi_k : mixture probabilities of different component ((n_cluster,) size numpy array)
    '''

    def __init__(self, n_cluster, init='k_means', max_iter=100, e=0.0001):
        self.n_cluster = n_cluster
        self.e = e
        self.max_iter = max_iter
        self.init = init
        self.means = None
        self.variances = None
        self.pi_k = None

    def fit(self, x):
        '''
            Fits a GMM to x.

            x: is a NXD size numpy array
            updates:
                self.means
                self.variances
                self.pi_k
        '''
        assert len(x.shape) == 2, 'x can only be 2 dimensional'

        np.random.seed(42)
        N, D = x.shape

        if (self.init == 'k_means'):
            # TODO
            # - comment/remove the exception
            # - initialize means using k-means clustering
            # - compute variance and pi_k (see P4.pdf)

            # DONOT MODIFY CODE ABOVE THIS LINE
            K = self.n_cluster
            mu_k, assign, _ = KMeans.fit(self, x)
            gamma_ik = np.zeros([N, K])
            gamma_ik[np.arange(N), assign[np.arange(N)]] = 1
            N_k = gamma_ik.sum(axis=0)
            sigma_k = np.zeros([K, D, D])
            for k in range(K):
                boo = x - mu_k[k]   # eq 7 x_i - mu_k vectorized
                sigma_k[k, :, :] = np.array([gamma_ik[i, k] * np.outer(boo[i], boo[i]) for i in range(N)]).sum(axis=0) / N_k[k]
            pi_k = np.zeros(K)
            pi_k = N_k / N
            self.means = mu_k
            self.variances = sigma_k
            self.pi_k = pi_k
            #raise Exception(
            #    'Implement initialization of variances, means, pi_k using k-means')
            # DONOT MODIFY CODE BELOW THIS LINE

        elif (self.init == 'random'):
            # TODO
            # - comment/remove the exception
            # - initialize means randomly
            # - initialize variance to be identity and pi_k to be uniform

            # DONOT MODIFY CODE ABOVE THIS LINE
            K = self.n_cluster
            mu_k = np.random.rand(K, D)
            sigma_k = np.zeros([K, D, D])
            sigma_k[np.arange(K), :, :] = np.eye(D)
            pi_k = np.zeros(K)
            pi_k[:] = 1 / K
            N_k = np.zeros(K)
            N_k[:] = N / K
            self.means = mu_k
            self.variances = sigma_k
            self.pi_k = pi_k
            gamma_ik = np.zeros([N, K])
            #raise Exception(
            #    'Implement initialization of variances, means, pi_k randomly')
            # DONOT MODIFY CODE BELOW THIS LINE

        else:
            raise Exception('Invalid initialization provided')

        # TODO
        # - comment/remove the exception
        # - Use EM to learn the means, variances, and pi_k and assign them to self
        # - Update until convergence or until you have made self.max_iter updates.
        # - Return the number of E/M-Steps executed (Int) 
        # Hint: Try to separate E & M step for clarity
        # DONOT MODIFY CODE ABOVE THIS LINE
        l = GMM.compute_log_likelihood(self, x)
        means = self.means
        variances = self.variances
        pi_k = self.pi_k

        for iter in range(self.max_iter):
            # E step
            # Avoid looping the instance and invert the matrix 1000 times by create k instances first
            inst = []
            for k in range(K):
                inst.append(GMM.Gaussian_pdf(means[k], variances[k, :, :]))
            Normal = np.array([[inst[k].getLikelihood(x[i, :]) for k in range(K)] for i in range(N)])
            gamma_ik = ((pi_k * Normal).T / (pi_k * Normal).sum(axis=1).T).T    # E step eq 4
            # M Step
            N_k = gamma_ik.sum(axis=0)
            for k in range(K):
                means[k] = np.multiply(x.T, gamma_ik[:, k]).sum(axis=1) / N_k[k]        # eq 6
            for k in range(K):
                boo = x - means[k]  # eq 7 x_i - mu_k vectorized
                variances[k, :, :] = np.array([gamma_ik[i, k] * np.outer(boo[i], boo[i]) for i in range(N)]).sum(
                    axis=0) / N_k[k]
            pi_k = N_k / N
            l_new = GMM.compute_log_likelihood(self, x)
            if np.absolute(l - l_new) < self.e:
                number_of_updates = iter
                break    # STOP
            l = l_new
        self.means = means
        self.variances = variances
        self.pi_k = pi_k
        return number_of_updates
        #raise Exception('Implement fit function (filename: gmm.py)')
        # DONOT MODIFY CODE BELOW THIS LINE

		
    def sample(self, N):
        '''
        sample from the GMM model

        N is a positive integer
        return : NXD array of samples

        '''
        assert type(N) == int and N > 0, 'N should be a positive integer'
        np.random.seed(42)
        if (self.means is None):
            raise Exception('Train GMM before sampling')

        # TODO
        # - comment/remove the exception
        # - generate samples from the GMM
        # - return the samples

        # DONOT MODIFY CODE ABOVE THIS LINE
        K = self.pi_k.shape[0]
        D = self.means.shape[1]
        k = np.random.choice(K, N, p=self.pi_k)
        samples = np.zeros([N, D])
        for n in range(N):
            samples[n, :] = np.random.multivariate_normal(self.means[k[n], :], self.variances[k[n], :, :])
        #raise Exception('Implement sample function in gmm.py')
        # DONOT MODIFY CODE BELOW THIS LINE
        return samples        

    def compute_log_likelihood(self, x, means=None, variances=None, pi_k=None):
        '''
            Return log-likelihood for the data

            x is a NXD matrix
            return : a float number which is the log-likelihood of data
        '''
        assert len(x.shape) == 2,  'x can only be 2 dimensional'
        if means is None:
            means = self.means
        if variances is None:
            variances = self.variances
        if pi_k is None:
            pi_k = self.pi_k    
        # TODO
        # - comment/remove the exception
        # - calculate log-likelihood using means, variances and pi_k attr in self
        # - return the log-likelihood (Float)
        # Note: you can call this function in fit function (if required)
        # DONOT MODIFY CODE ABOVE THIS LINE
        N, D = x.shape
        K = self.n_cluster
        normal = np.zeros([N, K])
        sumnormal = np.zeros(N)

        inst = []
        for k in range(K):
            inst.append(GMM.Gaussian_pdf(means[k], variances[k, :, :]))
        for i in range(N):
            for k in range(K):
                normal[i, k] = pi_k[k] * inst[k].getLikelihood(x[i, :])     # normal = pi_k * Normal function
        sumnormal = normal.sum(axis=1)

        log_likelihood = np.log(sumnormal[np.arange(N)]).sum().item()

        #raise Exception('Implement compute_log_likelihood function in gmm.py')

        # DONOT MODIFY CODE BELOW THIS LINE
        return log_likelihood

    class Gaussian_pdf():
        def __init__(self,mean,variance):
            self.mean = mean
            self.variance = variance
            self.c = None
            self.inv = None
            '''
                Input: 
                    Means: A 1 X D numpy array of the Gaussian mean
                    Variance: A D X D numpy array of the Gaussian covariance matrix
                Output: 
                    None: 
            '''
            # TODO
            # - comment/remove the exception
            # - Set self.inv equal to the inverse the variance matrix (after ensuring it is full rank - see P4.pdf)
            # - Set self.c equal to ((2pi)^D) * det(variance) (after ensuring the variance matrix is full rank)
            # Note you can call this class in compute_log_likelihood and fit
            # DONOT MODIFY CODE ABOVE THIS LINE
            D = np.shape(self.variance)[0]
            self.variance = (np.linalg.matrix_rank(variance[:, :]) < D).astype(int) * np.eye(D) * 0.001 + self.variance
            self.inv = np.linalg.inv(self.variance)
            self.c = ((2 * np.pi) ** D) * np.linalg.det(self.variance)
            #raise Exception('Impliment Guassian_pdf __init__')
            # DONOT MODIFY CODE BELOW THIS LINE

        def getLikelihood(self,x):
            '''
                Input: 
                    x: a 1 X D numpy array representing a sample
                Output: 
                    p: a numpy float, the likelihood sample x was generated by this Gaussian
                Hint: 
                    p = e^(-0.5(x-mean)*(inv(variance))*(x-mean)'/sqrt(c))
                    where ' is transpose and * is matrix multiplication
            '''
            #TODO
            # - Comment/remove the exception
            # - Calculate the likelihood of sample x generated by this Gaussian
            # Note: use the described implementation of a Gaussian to ensure compatibility with the solutions
            # DONOT MODIFY CODE ABOVE THIS LINE
            mean = self.mean
            inv = self.inv
            c = self.c
            boo = x - mean
            p = np.exp(- 0.5 * boo.T @ inv @ boo) / np.sqrt(c)

            #raise Exception('Impliment Guassian_pdf getLikelihood')
            # DONOT MODIFY CODE BELOW THIS LINE
            return p
