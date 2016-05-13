from collections import defaultdict
import click

def preProcess(run, ct):
    runfile = open(run)
    output_path = run + '_' + str(ct)
    output = open(output_path, 'w')
    while 1:
        line = runfile.readline()
        if not line:
            break
        else:
            result = line.split('\t')
            if int(result[1]) <= int(ct):
                output.write(line)
    return output_path



def loadGroundTruth(ground_truth, qrel):
    for line in qrel:
        elements = line.split()
        ground_truth[elements[0]].add(elements[2])


def computePrecisionAtRecall(ground_truth, runfile,):
    runfile = open(runfile, 'r')
    last_topic_id = None
    on_topic = 0
    precision_at_recall = {}

    for line in runfile:
        elements = line.split()

        if elements[0] != last_topic_id: # first line of the topic
            if last_topic_id:
                precision_at_recall[last_topic_id] = on_topic / float(dcount)
                #print last_topic_id, on_topic, dcount
            last_topic_id = elements[0]
            dcount = 1
            on_topic = 0
        else:
            dcount += 1

        if elements[2] in ground_truth[elements[0]]: on_topic += 1

    return sum(precision_at_recall.values()) / len(precision_at_recall)
    #return precision_at_recall

@click.command()
@click.option('-qrel', type=click.Path(exists=True))
@click.option('-run', type=click.Path(exists=True))
@click.option('-ct', type=click.INT)
def main(qrel, run, ct):
    qrel = open(qrel,'r')
    runfile = open(run, 'r')
    ground_truth = defaultdict(set)

    loadGroundTruth(ground_truth, qrel)

    print computePrecisionAtRecall(ground_truth, preProcess(run, ct))

main()
