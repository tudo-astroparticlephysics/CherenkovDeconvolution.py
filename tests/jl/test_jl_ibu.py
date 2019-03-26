import unittest, os
import numpy as np
import cherenkovdeconvolution.util as util
import cherenkovdeconvolution.methods.ibu as py_ibu

# import CherenkovDeconvolution with the alias 'jl_ibu' from Julia
from julia import CherenkovDeconvolution
jl_ibu = CherenkovDeconvolution # hack to achieve a lowercase alias unsupported by pyjulia..

@unittest.skipUnless(os.environ.get('TEST_JULIA')=='true', "Set TEST_JULIA=true to enable test")
class JlDseaTestSuite(unittest.TestCase):
    """Check the equivalence of DSEA between Python and Julia."""
    
    def test_jl_ibu_reverse_transfer(self):
        """Test the function cherenkovdeconvolution.methods.ibu._ibu_reverse_transfer."""
        for i in range(10):
            with self.subTest(i = i):
                I = np.random.randint(1, 100)
                J = np.random.randint(1, 1000)
                R = np.random.rand(J, I)
                f_0 = np.random.rand(I)
                py_B = py_ibu._ibu_reverse_transfer(R, f_0)
                jl_B = jl_ibu._ibu_reverse_transfer(R, f_0)
                np.testing.assert_allclose(py_B, jl_B)
    
    @unittest.skip('Not yet implemented')
    def test_jl_ibu(self):
        """Test complete deconvolution runs with IBU."""
        from sklearn.datasets import load_iris
        iris = load_iris()
        for i in range(10):
            p_iris = np.random.permutation(len(iris.target))
            X_data  = iris.data[p_iris[0:50], :]
            X_train = iris.data[p_iris[50:150], :]
            y_train = iris.target[p_iris[50:150]]
            np.testing.assert_allclose(py_f, jl_f)
            py_f = py_ibu.deconvolve_evt(x_data, x_train, y_train)
            jl_f = jl_ibu.ibu(x_data, x_train, y_train+1)
            np.testing.assert_allclose(py_f, jl_f)

if __name__ == '__main__':
    unittest.main()

