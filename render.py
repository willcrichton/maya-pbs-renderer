#!/opt/python/bin/python
import argparse, time, tempfile, subprocess, os, shutil

def die(err):
    print "Error: {}".format(err)
    exit(1)

MAX_TIME_PER_JOB = 60 * 20 # 20 min in default queue

def main():
    parser = argparse.ArgumentParser(
        description='Batch render a Maya scene.',
        epilog='Example usage: ./render.py -s -5 -e 100 -a "-cam my_camera" /home/wcrichto/final_proj scenes/final.mb')
    parser.add_argument('project', help='Absolute path of Maya project folder')
    parser.add_argument('scene', help='Path of scene to render relative to project')
    parser.add_argument('start', help='Starting frame to render', type=int)
    parser.add_argument('end', help='Ending frame to render', type=int)
    parser.add_argument('-t', '--time_per_frame', type=int, default=1,
                        help='Upper bound on render time per frame in minutes')
    parser.add_argument('-a', '--args', default='',
                        help='Additional arguments to pass to the Maya renderer.')
    parser.add_argument('-o', '--output', default='/home/wcrichto/maya-output',
                        help='Directory to output rendered frames to')
    args = parser.parse_args()

    if args.start > args.end:
        die("Start frame must be less than or equal to end frame")

    total_frames = args.end - args.start + 1
    total_time = total_frames * args.time_per_frame * 60
    jobs = max(total_time / MAX_TIME_PER_JOB, 1)
    frames_per_job = total_frames / jobs
    extra_frames = total_frames % jobs
    job_walltime = time.strftime('%H:%M:%S', time.gmtime(MAX_TIME_PER_JOB))

    # print "Frames %d, jobs %d, frames per job: %d" % (total_frames, jobs, frames_per_job)

    with open('template.job', 'r') as f: job_template = f.read()
    shutil.rmtree('jobs')
    os.makedirs('jobs')

    for i in xrange(jobs):
        job_start = i * frames_per_job + args.start
        job_end = job_start + frames_per_job - 1
        if i == jobs - 1: job_end += extra_frames
        format_args = {
            'walltime': job_walltime,
            'start': job_start,
            'end': job_end,
            'index': i,
            'args': args.args,
            'project': args.project,
            'scene': args.scene,
            'output': args.output
            }
        with open('jobs/maya_render_{}.job'.format(i), 'wb') as job_file:
            job_file.write(job_template.format(**format_args))
            #subprocess.check_call('qsub {}'.format(job_file.name), shell=True)


if __name__ == "__main__":
    main()
