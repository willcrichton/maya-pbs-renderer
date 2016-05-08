#!/opt/python/bin/python
import argparse, time, tempfile, subprocess, os, shutil, math

def die(err):
    print "Error: {}".format(err)
    exit(1)

MAX_TIME_PER_JOB = 60 * 60 * 2 # 2 hours in kayvon queue
NODES = []

for i in range(5, 31, 2):
    NODES.append('compute-0-{}'.format(i))

def main():
    parser = argparse.ArgumentParser(
        description='Batch render a Maya scene.',
        epilog='Example usage: ./render.py -s -5 -e 100 -a "-cam my_camera" /home/wcrichto/final_proj scenes/final.mb')
    parser.add_argument('project', help='Absolute path of Maya project folder')
    parser.add_argument('scene', help='Path of scene to render relative to project')
    parser.add_argument('start', help='Starting frame to render', type=int)
    parser.add_argument('end', help='Ending frame to render', type=int)
    parser.add_argument('-s', '--skip', type=int, default=1, help='Render every X frames')
    parser.add_argument('-t', '--time_per_frame', type=int, default=60,
                        help='Upper bound on render time per frame in seconds')
    parser.add_argument('-m', '--max_time_per_job', type=int, default=MAX_TIME_PER_JOB,
                        help='Maximum time in seconds allowed for each job')
    parser.add_argument('-o', '--output', default='/home/wcrichto/maya-output',
                        help='Directory to output rendered frames to')
    parser.add_argument('-a', '--args', default='',
                        help='Additional arguments to pass to the Maya renderer.')
    args = parser.parse_args()

    if args.start > args.end:
        die("Start frame must be less than or equal to end frame")

    args.time_per_frame /= args.skip
    total_frames = (args.end - args.start + 1)
    frames_per_job = args.max_time_per_job / args.time_per_frame
    jobs = int(math.ceil(float(total_frames) / frames_per_job))
    extra_frames = total_frames % frames_per_job
    job_walltime = time.strftime('%H:%M:%S', time.gmtime(frames_per_job * args.time_per_frame))

    with open('template.job', 'r') as f: job_template = f.read()
    if os.path.isdir('jobs'): shutil.rmtree('jobs')
    os.makedirs('jobs')

    for i in xrange(jobs):
        job_start = i * frames_per_job + args.start
        if i == jobs - 1: job_end = job_start + extra_frames - 1
        else: job_end = job_start + frames_per_job - 1
        format_args = {
            'walltime': job_walltime,
            'start': job_start,
            'end': job_end,
            'index': '{:02d}'.format(i),
            'args': args.args,
            'project': args.project,
            'scene': args.scene,
            'output': args.output,
            'node': NODES[i % len(NODES)],
            'skip': args.skip
            }
        with open('jobs/maya_render_{:02d}.job'.format(i), 'wb') as job_file:
            job_file.write(job_template.format(**format_args))

if __name__ == "__main__":
    main()
