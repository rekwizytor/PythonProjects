import argparse
from ising import Ising


parser = argparse.ArgumentParser()
parser.add_argument('n_size', type=int, help='number of rows')
parser.add_argument('m_size', type=int, help='number of columns')
parser.add_argument('--J', type=float, default=1.0, help='coupling constant')
parser.add_argument('--beta', type=float, default=1.0, help='inverse temperature')
parser.add_argument('--B', type=float, default=1.0, help='external magnetic field')
parser.add_argument('--n_steps', type=int, default=10, help='number of simulation steps')
parser.add_argument('--spin_density', type=float, default=0.5, help='initial spin density')
parser.add_argument('--image_name', type=str, default=None, help='label of the image files')
parser.add_argument('--gif_name', type=str, default=None, help='name of the GIF file')
parser.add_argument('--magn_name', type=str, default=None, help='name of the magnetization file')
args = parser.parse_args()

i1 = Ising(args.n_size, args.m_size, args.J, args.beta, args.B, args.n_steps, args.spin_density,
            args.image_name, args.gif_name, args.magn_name)
i1.run()