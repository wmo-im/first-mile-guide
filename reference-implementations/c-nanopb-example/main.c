#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include "pb_encode.h"
#include "firstmile.pb.h"


/*
    The following message is encoded by this simple demo:

    {
        "observations": 
        [
            {
                "parameterDefinitionId": 1,    
                "values": 
                [
                    {
                        "floatValue": 23.5
                    },
                    {
                        "emptyValue": {}
                    }
                ],                
                "time": {
                    "seconds": 1759343541,
                    "nanos": 0
                }
            }
        ]
    }
*/

static wmo_firstmile_poc1_Observation observations[1];
static wmo_firstmile_poc1_Value values[2];

bool encode_values(pb_ostream_t *stream, const pb_field_t *field, void * const *arg);

bool encode_observations(pb_ostream_t *stream, const pb_field_t *field, void * const *arg) {
    wmo_firstmile_poc1_Observation *obs = &observations[0];

    time_t current_time = time(NULL);
    obs->parameterDefinitionId = 1;
    obs->has_time = true;
    obs->time.seconds = current_time;
    obs->time.nanos = 0;

    obs->values.funcs.encode = &encode_values;
    obs->values.arg = NULL;

    if (!pb_encode_tag_for_field(stream, field))
        return false;

    return pb_encode_submessage(stream, wmo_firstmile_poc1_Observation_fields, obs);
}

bool encode_values(pb_ostream_t *stream, const pb_field_t *field, void * const *arg) {
    values[0].which_kind = wmo_firstmile_poc1_Value_floatValue_tag;
    values[0].kind.floatValue = 23.5f;

    values[1].which_kind = wmo_firstmile_poc1_Value_emptyValue_tag;

    for (int i = 0; i < 2; i++) {
        if (!pb_encode_tag_for_field(stream, field))
            return false;
        if (!pb_encode_submessage(stream, wmo_firstmile_poc1_Value_fields, &values[i]))
            return false;
    }

    return true;
}

int main() {
    uint8_t buffer[1024];
    pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));

    wmo_firstmile_poc1_Data data = wmo_firstmile_poc1_Data_init_zero;

    data.observations.funcs.encode = &encode_observations;
    data.observations.arg = NULL;

    bool status = pb_encode(&stream, wmo_firstmile_poc1_Data_fields, &data);
    size_t message_length = stream.bytes_written;

    if (!status) {
        fprintf(stderr, "Encoding failed: %s\n", PB_GET_ERROR(&stream));
        return 1;
    }

    for (size_t i = 0; i < message_length; i++) {
        printf("%02X", buffer[i]);
    }
    printf("\n");

    return 0;
}