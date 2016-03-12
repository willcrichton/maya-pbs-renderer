#!python
import argparse, time, tempfile, subprocess

def die(err):
    print "Error: {}".format(err)
    exit(1)

def main():
    parser = argparse.ArgumentParser(description='Batch render a Maya scene.', epilog='Example usage: ./render.py -s -5 -e 100 -a "-cam my_camera" ~/final_proj/scenes/final.mb')
    parser.add_argument('-s', '--start', help='Starting frame to render', required=True, type=int)
    parser.add_argument('-e', '--end', help='Ending frame to render', required=True, type=int)
    parser.add_argument('-j', '--jobs', help='Number of jobs to use for rendering', type=int, default=4)
    parser.add_argument('-t', '--time_per_frame', help='Reasonable upper bound on render time per frame', type=int, default=30)
    parser.add_argument('-a', '--args', help='Additional arguments to pass to the Maya renderer.', default='')
    parser.add_argument('scene_path', help='Path of scene to render')
    args = parser.parse_args()

    if args.start > args.end: die("Start frame must be less than or equal to end frame")
    if args.jobs <= 0: die("Must have more than zero jobs")
    
    total_frames = args.end - args.start + 1
    frames_per_job = total_frames / args.jobs
    extra_frames = total_frames % args.jobs
    job_walltime = time.strftime('%H:%M:%S', time.gmtime(frames_per_job * args.time_per_frame))

    with open('template.job', 'r') as f: job_template = f.read()

    for i in xrange(args.jobs):
        job_start = i * frames_per_job + args.start
        job_end = job_start + frames_per_job - 1
        if i == args.jobs - 1: job_end += extra_frames
        format_args = {
            'walltime': job_walltime,
            'start': job_start,
            'end': job_end,
            'index': i,
            'args': args.args,
            'file': args.scene_path
            }
        with tempfile.NamedTemporaryFile() as job_file:
            job_file.write(job_template.format(**format_args))
            subprocess.check_call("qsub {}".format(job_file.name), shell=True)
        

if __name__ == "__main__":
    main()
