from string import Template

from app_config import AppConfig


class ReconciliationFeedType:

    def __init__(self):
        self.config = AppConfig({})

    def path_from(self, template_name):
        rec_base_path = 'resources/reconciliation-templates/'
        return '{}/{}.xml'.format(rec_base_path, template_name)

    def get_rec_params(self, feed_type):
        if feed_type == 'AMBREC':
            return self.path_from('ambrec-template'), self.config.amb_schemas()['xmlns:ns']
        elif feed_type == 'INTREC':
            return self.path_from('intrec-template'), self.config.integrated_schemas()['xmlns:ns']
        elif feed_type == 'CSREC':
            return self.path_from('csrec-template'), self.config.integrated_schemas()['xmlns:ns']

        raise AttributeError("invalid feed_type for rec. feed_type: {}".format(feed_type))

    def generate_file_for(self, feed_type, organisation, filename):
        template_path, xmlns_ns = self.get_rec_params(feed_type)

        content = {
            "ORGANISATION": organisation,
            "XMLNS_NS": xmlns_ns
        }

        # open the file
        filein = open(template_path)
        # read it
        src = Template(filein.read())
        # do the substitution
        result = src.substitute(content)
        # write the results into new file
        self.write_file(result, filename)

    def write_file(self, content, filename):
        with open(filename, "w") as text_file:
            text_file.write(content)
