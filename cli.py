import click
import logging
import helpers

@click.command()
@click.option('--config_file', help='Path to SnapperDB instance configuration file')
@click.option('--id_file', help='Path to text file containing all samples to add to SnapperDB instance')
@click.option('--work_dir', help='Path to SnapperDB database working directory')
def cli(config_file, id_file, work_dir):
    logging.basicConfig(
        format='\033[92m \033[1m %(asctime)s \033[0m %(message)s ',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    # Gather and link files from text file (id_file) to {work_dir}/fastq_links
    fastq_folder_path, filtered_id_list = helpers.link_files(id_file, work_dir)

    # Prepare dictionary with {sample_id:[R1,R2],} format
    sample_dictionary = helpers.get_sample_dictionary(fastq_folder_path)

    # Filter dictionary to only new stuff is added to update script
    filtered_sample_dictionary = {}
    for key, value in sample_dictionary.items():
        if key in filtered_id_list:
            logging.info('Detected new sample: {}'.format(key))
            filtered_sample_dictionary[key] = value
        else:
            logging.info('{} already in SnapperDB --- skipped'.format(key))

    # Make shell script
    helpers.prepare_db_update_script(config_file=config_file,
                                     work_dir=work_dir,
                                     sample_dictionary=filtered_sample_dictionary)

    logging.info('Script complete')

if __name__ == '__main__':
    cli()