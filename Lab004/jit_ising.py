from numba import njit
import numpy as np
from PIL import Image, ImageDraw
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn, TimeElapsedColumn
import rich.traceback
import rich

@njit
def calc_H(spins, J, B):
    tmpH = 0
    for i in range(spins.shape[0]):
        for j in range(spins.shape[1]):
            spin = spins[i, j]
            tmpH -= J * spin * spins[(i + 1) % spins.shape[0], j]
            tmpH -= J * spin * spins[i, (j + 1) % spins.shape[1]]
            tmpH -= B * spin
    return tmpH

@njit
def calc_magnetization(spins):
    return np.sum(spins) / (spins.shape[0] * spins.shape[1])
    
def save_magnetization(magnetization, step, magn_name = None):
    if magn_name is not None:
        with open(f'{magn_name}.txt', 'a') as f:
            f.write(f'{step}\t{np.round(magnetization, 2)}\n')

@njit
def change_random_spin(spins):
    tmp_spins = spins.copy()
    random_i = np.random.randint(0, spins.shape[0])
    random_j = np.random.randint(0, spins.shape[1])
    tmp_spins[random_i, random_j] = -spins[random_i, random_j]
    return tmp_spins
    
def gen_image(spins, images, image_name = None):    
    image = Image.new('RGB', (1000, 1000), 'white')
    draw = ImageDraw.Draw(image)
    n_width = 1000 / spins.shape[0]
    m_width = 1000 / spins.shape[1]
    for i in range(spins.shape[0]):
        for j in range(spins.shape[1]):
            x = n_width * i
            y = m_width * j
            sign = spins[i, j]
            if sign == 1:
                draw.rectangle([x, y, x + n_width, y + m_width], fill='red')
            else:
                draw.rectangle([x, y, x + n_width, y + m_width], fill='blue')
    images.append(image)
    if image_name is not None:
        image.save(f'images/{image_name}.png')

def gen_gif(images, image_name = None, gif_name = None):
    if gif_name is not None:
        images[0].save(f'{gif_name}.gif', save_all=True, append_images=images[1:], loop=0, duration=200)
    
def run(n_size, m_size, J = 1.0, beta = 1.0, B = 1.0, n_steps = 10, spin_density = 0.5, image_name = None,
        gif_name = None, magn_name = None):
    n_size = n_size
    m_size = m_size
    J = J
    beta = beta
    B = B
    n_steps = n_steps
    spin_density = spin_density
    image_name = image_name
    gif_name = gif_name
    magn_name = magn_name
    spins = np.random.choice([-1, 1], size=(n_size, m_size), p=[1 - spin_density, spin_density])
    images = []

    rich.traceback.install()
    rich.get_console().clear()

    H = calc_H(spins, J, B)
    magnetization = calc_magnetization(spins)
    save_magnetization(magnetization, 0, magn_name)
    gen_image(spins, images, f'{image_name}_0')

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("Elapsed time: "),
        TimeElapsedColumn(),
        TextColumn("Remaining time: "),
        TimeRemainingColumn(),
    ) as progress:

        task1 = progress.add_task("Running simulation...", total=n_steps)
        for step in range(n_steps):
            for i in range(n_size + m_size):
                new_spins = change_random_spin(spins)
                new_H = calc_H(new_spins, J, B)
                deltaE = new_H - H
                if deltaE < 0:
                    spins = new_spins
                    H = new_H
                else:
                    if np.random.rand() < np.exp(-beta * deltaE):
                        spins = new_spins
                        H = new_H

            gen_image(spins, images, f'{image_name}_{step+1}')

            magnetization = calc_magnetization(spins)
            save_magnetization(magnetization, step + 1, magn_name)

            progress.advance(task1)

        if gif_name is not None:
            task2 = progress.add_task("Generating GIF...", total=1)
            gen_gif(images, image_name, gif_name)
            progress.advance(task2)
