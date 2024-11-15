import numpy as np
from PIL import Image, ImageDraw
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn
import rich.traceback
import rich


class Ising:
    def __init__(self, n_size, m_size, J = 1.0, beta = 1.0, B = 1.0, n_steps = 10, spin_density = 0.5,
                image_name=None, gif_name=None, magn_name=None):
        self.n_size = n_size
        self.m_size = m_size
        self.J = J
        self.beta = beta
        self.B = B
        self.n_steps = n_steps
        self.spin_density = spin_density
        self.image_name = image_name
        self.gif_name = gif_name
        self.magn_name = magn_name
        self.spins = np.random.choice([-1, 1], size=(n_size, m_size), p=[1 - spin_density, spin_density])
        self.images = []

    def calc_H(self, spins):
        tmpH = 0
        for i in range(self.n_size):
            for j in range(self.m_size):
                spin = spins[i, j]
                tmpH -= self.J * spin * spins[(i + 1) % self.n_size, j]
                tmpH -= self.J * spin * spins[i, (j + 1) % self.m_size]
                tmpH -= self.B * spin
        return tmpH
    
    def calc_magnetization(self, spins):
        return np.sum(spins) / (self.n_size * self.m_size)
    
    def save_magnetization(self, magnetization, step):
        if self.magn_name is not None:
            with open(f'{self.magn_name}.txt', 'a') as f:
                f.write(f'{step}\t{np.round(magnetization, 2)}\n')

    def change_random_spin(self):
        tmp_spins = self.spins.copy()
        random_i = np.random.randint(0, self.n_size)
        random_j = np.random.randint(0, self.m_size)
        tmp_spins[random_i, random_j] = -self.spins[random_i, random_j]
        return tmp_spins
    
    def gen_image(self, image_name):
        if self.image_name is not None:
            image = Image.new('RGB', (1000, 1000), 'white')
            draw = ImageDraw.Draw(image)
            n_width = 1000 / self.n_size
            m_width = 1000 / self.m_size
            for i in range(self.n_size):
                for j in range(self.m_size):
                    x = n_width * i
                    y = m_width * j
                    sign = self.spins[i, j]
                    if sign == 1:
                        draw.rectangle([x, y, x + n_width, y + m_width], fill='red')
                    else:
                        draw.rectangle([x, y, x + n_width, y + m_width], fill='blue')
            self.images.append(image)
            image.save(f'images/{image_name}.png')

    def gen_gif(self):
        if self.image_name is not None and self.gif_name is not None:
            self.images[0].save(f'{self.gif_name}.gif', save_all=True, append_images=self.images[1:], loop=0, duration=200)
    
    def run(self):
        rich.traceback.install()
        rich.get_console().clear()

        H = self.calc_H(self.spins)
        magnetization = self.calc_magnetization(self.spins)
        self.save_magnetization(magnetization, 0)
        self.gen_image(f'{self.image_name}_0')

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TextColumn("Elapsed time: "),
            TimeElapsedColumn(),
            TextColumn("Remaining time: "),
            TimeRemainingColumn(),
        ) as progress:

            task1 = progress.add_task("Running simulation...", total=self.n_steps)
            for step in range(self.n_steps):
                for i in range(self.n_size + self.m_size):
                    new_spins = self.change_random_spin()
                    new_H = self.calc_H(new_spins)
                    deltaE = new_H - H
                    if deltaE < 0:
                        self.spins = new_spins
                        H = new_H
                    else:
                        if np.random.rand() < np.exp(-self.beta * deltaE):
                            self.spins = new_spins
                            H = new_H

                self.gen_image(f'{self.image_name}_{step+1}')

                magnetization = self.calc_magnetization(self.spins)
                self.save_magnetization(magnetization, step + 1)

                progress.advance(task1)

            if self.image_name is not None and self.gif_name is not None:
                task2 = progress.add_task("Generating GIF...", total=1)
                self.gen_gif()
                progress.advance(task2)
