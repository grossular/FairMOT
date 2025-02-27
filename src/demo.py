from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import _init_paths

import logging
import os, sys
import os.path as osp
from opts import opts
from tracking_utils.utils import mkdir_if_missing
from tracking_utils.log import logger
import datasets.dataset.jde as datasets
from track import eval_seq


logger.setLevel(logging.INFO)


def demo(opt):
    result_root = opt.output_root if opt.output_root != '' else '.'
    mkdir_if_missing(result_root)
    file_name = osp.basename(opt.input_video).split('.')[0].replace(' ', '_')
    model_name = osp.basename(opt.load_model).split('.')[0]
    base_name = f'{file_name}_{model_name}_{opt.conf_thres}'

    logger.info('Starting tracking...')
    logger.info(f'Working on: {opt.input_video}')
    dataloader = datasets.LoadVideo(opt.input_video, opt.img_size)
    result_filename = os.path.join(result_root, f'{base_name}_results.txt')
    frame_rate = dataloader.frame_rate

    frame_dir = None if opt.output_format == 'text' else osp.join(result_root, f'{file_name}-frames')
    eval_seq(opt, dataloader, 'kitti', result_filename, save_dir=frame_dir, show_image=False, frame_rate=frame_rate)

    if opt.output_format == 'video':
        output_video_path = osp.join(result_root, f'{base_name}_result.mp4')
        cmd_str = 'ffmpeg -f image2 -i {}/%05d.jpg -b 5000k -c:v mpeg4 {}'.format(osp.join(result_root, f'{file_name}-frames'), output_video_path)
        os.system(cmd_str)


if __name__ == '__main__':
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    opt = opts().init()
    demo(opt)
